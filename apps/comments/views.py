from django.contrib import messages
from django.shortcuts import redirect

from apps.comments.forms import CommentCreateForm


def create_comment(request):
    """
    Handles the creation of a new product comment.

    Validates and saves the comment form, displaying appropriate success or error messages.
    Redirects the user back to the page from where the request originated.

    Args:
        request (HttpRequest): The HTTP request object containing the form data.

    Returns:
        HttpResponseRedirect: Redirects the user back to the referring page, or 404 if the method is GET.
    """
    if request.method == 'GET':
        # If the request method is GET, redirect to the 404 page
        return redirect('404-page')

    form = CommentCreateForm(data=request.POST)

    if form.is_valid():
        # If the form is valid, save the comment and show a success message
        form.save()
        messages.success(request, 'Your comment has been created!')
    else:
        # If the form is invalid, show the form errors
        messages.error(request, form.errors)

    # Get the referring URL and remove any query parameters
    url = request.META.get('HTTP_REFERER')
    url = url.split('?')[0]

    # Redirect the user back to the referring page
    return redirect(url)
