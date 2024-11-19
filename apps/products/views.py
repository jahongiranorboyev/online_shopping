from decimal import Decimal
from itertools import product
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from apps.cart.models import Cart
from apps.comments.models import ProductComment
from apps.features.models import Feature, FeatureValue
from apps.products.models import Product
from apps.wishlist.models import Wishlist


def product_detail(request, pk):
    """
    View to display the detailed page of a product, including comments and features.
    """
    product = get_object_or_404(Product, pk=pk)
    comments = ProductComment.objects.filter(product_id=product.id).order_by('-created_at')

    # Handle pagination for comments
    comment_page = request.GET.get('comment_page', 1)
    comment_page_obj = Paginator(comments, 3).get_page(comment_page)

    # Handle cart quantity for authenticated users
    if not request.user.is_authenticated:
        user_cart_quantity = 0
    else:
        try:
            user_cart_quantity = Cart.objects.get(user=request.user, product_id=pk).quantity
        except Cart.DoesNotExist:
            user_cart_quantity = 0

    # Increment product view count on GET request
    if request.method == 'GET':
        product.seen_count += 1

    # Context for rendering the product detail page
    context = {
        'product': product,
        'comments': comments,
        'comment_page': comment_page_obj,
        'features': product.features,
        'user_cart_quantity': user_cart_quantity,
        'page': 'detail',
    }
    return render(request=request, template_name='detail.html', context=context)


def product_by_feature(request, pk):
    """
    Redirects to the product detail page based on the feature filter.
    """
    return redirect('products:detail-page', pk=pk)


def product_list(request: WSGIRequest) -> HttpResponse:
    """
    Displays the product list with filtering options for categories, search, and features.
    """
    user = request.user
    user_cart = []
    user_wishlist = []

    # Handle cart and wishlist for authenticated users
    if user.is_authenticated:
        user_cart = Cart.objects.filter(user=user).values_list('product', flat=True)
        user_wishlist = Wishlist.objects.filter(user=user).values_list('product', flat=True)

    # Store cart and wishlist in session
    request.session['user_cart'] = list(user_cart)
    request.session['user_wishlist'] = list(user_wishlist)

    # Retrieve search text and category ID from session
    search_text = request.session.get('search_text', None)
    cat_id = request.session.get('cat_id', None)
    queryset = Product.objects.order_by('-pk')

    features = []
    if cat_id:
        # Retrieve features related to the category
        features = Feature.objects.filter(category_id=cat_id).prefetch_related('values')

        # Retrieve feature values with product count
        feature_values = FeatureValue.objects.filter(
            feature__category_id=cat_id
        ).annotate(products_count=Count('product_features_values')).select_related('feature')

        features = {}
        for feature_value in feature_values:
            item = {
                'pk': str(feature_value.pk),
                'name': feature_value.name,
                'products_count': feature_value.products_count,
            }
            if feature_value.feature.pk not in features:
                features[feature_value.feature.pk] = {
                    'pk': str(feature_value.feature.pk),
                    'name': feature_value.feature.name,
                    'values': [item]
                }
            else:
                features[feature_value.feature.pk]['values'].append(item)

        features = list(features.values())

    # Search functionality for product titles
    if search_text:
        queryset = queryset.filter(title__icontains=search_text)

    # Handle filters based on date, rating, and views
    data = request.GET.get('date')
    rating = request.GET.get('rating')
    views = request.GET.get('views')

    if data:
        try:
            # Convert the date string to a timezone-aware datetime
            naive_date = timezone.datetime.strptime(data, "%Y-%m-%d")
            aware_date = timezone.make_aware(naive_date, timezone.get_current_timezone())
            queryset = queryset.filter(created_at=aware_date)
        except ValueError:
            pass

    filters = Q()
    if rating:
        try:
            rating_value = Decimal(rating) if rating else None
            if rating_value is not None:
                filters &= Q(avg_rating=rating_value)
        except (ValueError, TypeError):
            pass

    if views:
        try:
            views_value = int(views) if views else None
            if views_value is not None:
                filters &= Q(seen_count=views_value)
        except (ValueError, TypeError):
            pass

    # Apply filters to queryset
    if filters:
        queryset = queryset.filter(filters)

    # Pagination setup for product listing
    page_number = request.GET.get('page', 1)
    paginate_obj = Paginator(queryset, 9)
    page_obj = paginate_obj.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page': 'shop',
        'user_wishlist': user_wishlist,
        'user_cart': user_cart,
        'features': features if cat_id else {},
    }

    return render(request=request, template_name='shop.html', context=context)
