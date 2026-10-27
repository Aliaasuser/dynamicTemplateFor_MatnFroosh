from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.
def view_public_header(request: HttpRequest):
    context = {
        'url_name' : request.resolver_match.url_name,
    }
    return render(request, 'header_module/public_header.html', context=context)