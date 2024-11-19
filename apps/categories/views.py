from django.shortcuts import render, redirect
from apps.categories.models import Category


def category(request):
    """
    Renders a list of all categories and passes them to the template.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered 'index.html' template with the context containing all categories.
    """
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'index.html', context)


def set_category(request, cat_id):
    """
    Sets the selected category in the session, if the category exists.

    Args:
        request (HttpRequest): The incoming HTTP request.
        cat_id (int): The ID of the category to be selected.

    Returns:
        HttpResponseRedirect: Redirects to the 'products:product_list' page.
    """
    # Check if the category ID exists in the Category table
    if cat_id in Category.objects.values_list('pk', flat=True):
        request.session['cat_id'] = cat_id
    else:
        request.session['cat_id'] = None

    return redirect('products:product_list')
