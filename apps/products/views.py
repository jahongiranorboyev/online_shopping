from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from apps.products.models import Product

def detail(request):
    return render(request=request, template_name='detail.html', context={'page': 'detail'})


def product_list(request: WSGIRequest) -> HttpResponse:
    search_text = request.session.get('search_text',None)
    queryset= Product.objects.order_by('-pk')

    if search_text:
        queryset = queryset.filter(title__icontains=search_text).order_by('-pk'),

    page_number = request.GET.get('page', 1)
    page_number = int(page_number)
    paginate_obj = Paginator( queryset,9)
    page_obj = paginate_obj.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'page': 'shop',
    }
    return render(request=request, template_name='shop.html', context=context)
