from pyexpat import features

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from apps.cart.models import Cart
from apps.comments.models import ProductComment
from apps.features.models import Feature
from apps.products.models import Product, ProductFeature
from apps.wishlist.models import Wishlist


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = ProductComment.objects.filter(product_id=product.id).order_by('-created_at')
    comment_page = request.GET.get('comment_page', 1)
    comment_page_obj = Paginator(comments, 3).get_page(comment_page)

    product_features = ProductFeature.objects.prefetch_related('feature_values').filter(product_id = pk)
    features ={}
    for product_feature in product_features:
        for value in product_feature.feature_values.all():
            if value.feature_id not in features:
                features[value.feature_id] = {
                    'id': value.feature_id,
                    'name': value.feature.name,
                    'values':[
                        {'id':value.id, 'name':value.name},
                    ]
                }
            else:
                features[value.feature_id]['values'].append({'id':value.id, 'name':value.name})


    context = {
        'product': product,
        'comments': comments,
        'comment_page': comment_page_obj,
        'features': list(features.values()),
        'page': 'detail',
    }
    return render(request=request, template_name='detail.html', context=context)


def product_by_feature(request, pk):
    print(request.POST)
    return redirect('products:detail-page', pk=pk)


def product_list(request: WSGIRequest) -> HttpResponse:
    user = request.user
    if user.is_authenticated:
        user_cart = Cart.objects.filter(user=user).values_list('product', flat=True)
        user_wishlist = Wishlist.objects.filter(user=user).values_list('product', flat=True)
    else:
        user_cart = []
        user_wishlist = []

    search_text = request.session.get('search_text', None)
    cat_id = request.session.get('cat_id', None)
    queryset = Product.objects.order_by('-pk')

    if cat_id:
        queryset = queryset.filter(Q(category_id=cat_id) | Q(category__parent_id=cat_id))

    if search_text:
        queryset = queryset.filter(title__icontains=search_text)

    page_number = request.GET.get('page', 1)
    paginate_obj = Paginator(queryset, 9)
    page_obj = paginate_obj.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'page': 'shop',
        'user_wishlist': user_wishlist,
        'user_cart': user_cart,
    }
    return render(request=request, template_name='shop.html', context=context)
