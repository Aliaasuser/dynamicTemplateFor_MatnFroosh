from django.shortcuts import render
from django.http import HttpRequest
from . import models

# Create your views here.
def view_public_header(request: HttpRequest):
    header_navbar_links = models.HeaderNavbarLinks_model.objects.filter(father=None, is_active=True)
    hnls = []
    for hnl in header_navbar_links:
        hnls.append({
            'text' : hnl.text,
            'url_name' : hnl.url_name,
            'url' : hnl.url,
            'more_classes' : hnl.more_classes,
            'subobjs' : hnl.headernavbarlinks_model_set.filter(is_active=True),
        })
    context = {
        'url_name' : request.resolver_match.url_name,
        'url' : request.build_absolute_uri(),
        'header_main_links' : models.HeaderMainLinks_model.objects.filter(father=None, is_active=True),
        'logo' : models.HeaderLogo_model.objects.filter(is_active=True).first(),
        'header_navbar_links' : hnls,
    }
    return render(request, 'header_module/public_header.html', context=context)

def view_hml_has_submenu(request: HttpRequest, componentAddress: str, hml_obj: models.HeaderMainLinks_model):
    context = {
        'hml_obj' : {
            'text' : hml_obj.text,
            'title' : hml_obj.title,
            'url_name' : hml_obj.url_name,
            'url' : hml_obj.url,
            'subobjs' : hml_obj.headermainlinks_model_set.filter(is_active=True),
        },
        'url_name' : request.resolver_match.url_name,
        'url' : request.build_absolute_uri(),
    }
    return render(request, componentAddress, context=context)