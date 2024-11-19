from django.contrib import messages
from django.shortcuts import render, redirect

from apps.contact.forms import ContactCreateForm


def contact(request):
    """
    Renders the contact page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered contact page.
    """
    return render(
        request=request,
        template_name='contact.html',
        context={'page': 'contact'}
    )


def create_contact(request):
    """
    Handles the creation of a new contact message from the contact form.

    If the form is valid, saves the message and displays a success message.
    Otherwise, displays error messages.

    Args:
        request (HttpRequest): The HTTP request object containing form data.

    Returns:
        HttpResponseRedirect: Redirects to the referring URL after processing the form.
    """
    if request.method == 'GET':
        return redirect('404-page')

    form = ContactCreateForm(data=request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'Your message has been sent!')
    else:
        messages.error(request, form.errors)

    # Redirects to the referring URL
    return redirect(request.META.get('HTTP_REFERER'))
