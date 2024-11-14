from decimal import Decimal

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from apps.cart.models import Cart
from apps.comments.models import ProductComment
from apps.features.models import Feature
from apps.products.models import Product
from apps.wishlist.models import Wishlist


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = ProductComment.objects.filter(product_id=product.id).order_by('-created_at')
    comment_page = request.GET.get('comment_page', 1)
    comment_page_obj = Paginator(comments, 3).get_page(comment_page)
    if not request.user.is_authenticated:
        user_cart_quantity = 0
    else:
        try:
            user_cart_quantity = Cart.objects.get(user=request.user, product_id=pk).quantity
        except Cart.DoesNotExist:
            user_cart_quantity = 0

    if request.method == 'GET':
        product.seen_count += 1




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
    return redirect('products:detail-page', pk=pk)




def product_list(request: WSGIRequest) -> HttpResponse:
    user = request.user
    if user.is_authenticated:
        user_cart = Cart.objects.filter(user=user).values_list('product', flat=True)
        user_wishlist = Wishlist.objects.filter(user=user).values_list('product', flat=True)
    else:
        user_cart = []
        user_wishlist = []
    request.session['user_cart'] = list(user_cart)
    request.session['user_wishlist'] = list(user_wishlist)


    search_text = request.session.get('search_text', None)
    cat_id = request.session.get('cat_id', None)
    queryset = Product.objects.order_by('-pk')
    features = []
    if cat_id:
        features = Feature.objects.filter(category_id=cat_id).prefetch_related('feature_values')
        queryset = queryset.filter(Q(category_id=cat_id) | Q(category__parent_id=cat_id))

    if search_text:
        queryset = queryset.filter(title__icontains=search_text)

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


    if filters:
        queryset = queryset.filter(filters)



    page_number = request.GET.get('page', 1)
    paginate_obj = Paginator(queryset, 9)
    page_obj = paginate_obj.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'page': 'shop',
        'user_wishlist': user_wishlist,
        'user_cart': user_cart,
        'features': features,
    }
    return render(request=request, template_name='shop.html', context=context)
