from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpRequest, JsonResponse, Http404
from . import models

# Create your views here.

def comments_section(request: HttpRequest, slug: str):
    if request.method == 'GET':
        comments = models.CommentForProduct_model.objects.exclude(text='').select_related('product').filter(product__slug=slug, is_active=True).select_related('user').select_related('father').select_related('score')
        context = {
            'current_user' : request.user,
            'comments' : comments[:1],
            'is_complete' : comments.count() <= 1,
        }
        return render(request, 'comment_module/comments_section.html', context=context)
    else:
        pass

def get_more_comments_for_product(request: HttpRequest, slug: str):
    if request.method != 'GET':
        raise Http404()
    comments = models.CommentForProduct_model.objects.exclude(text='').select_related('product').filter(product__slug=slug, is_active=True).select_related('user').select_related('father').select_related('score')
    resize = request.GET.get('show-more-than')
    try:
        resize = int(resize) + 10
    except:
        raise Http404()
    if resize < 10:
        raise Http404()
    is_complete = comments.count() <= resize
    comments = comments[:resize]
    if comments == None:
        raise Http404()
    output = ''
    for comment in comments:
        output += render_to_string('comment_module/components/sample_comment.html', {'comment' : comment, 'current_user' : request.user,}) + '\n'

    return JsonResponse({'htmlResponse' : output, 'is_complete' : is_complete,})