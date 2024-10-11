from django.shortcuts import render

def contact(request):
    return render(request=request, template_name='contact.html', context={'page': 'contact'})
