from django.shortcuts import render
from django.http import HttpRequest, Http404
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from django.core.paginator import Page
from . import models
from account_module.models import User, UserGroup_model, UserConnectorToUserGroup

# Create your views here.
class ShopPage_view(ListView):
    template_name = 'product_module/shop_page.html'
    queryset = models.Product_model.objects.filter(is_active=True, is_deleted=False)
    ordering = ['-rating', 'price']
    context_object_name = 'products'
    paginate_by = 12
    paginate_orphans = 2

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('owner').prefetch_related(Prefetch(
            'owner__group_connectors',
            queryset=UserConnectorToUserGroup.objects.filter(
                user_group_id=UserGroup_model.objects.get(title='products_owners').pk
            ),
            to_attr='connector_to_powners'
        )).prefetch_related(Prefetch(
            'tags',
            queryset=models.ProductTag_model.objects.filter(is_active=True),
            to_attr='joined_tags'
        ))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj: Page = context.get('page_obj')
        range_size = 7
        is_pre_ellipsis = False
        is_next_ellipsis = False
        range_start = 0
        range_end = 0
        if (page_obj.number - int((range_size - 1) / 2) > 1):
            is_pre_ellipsis = True
            range_start = page_obj.number - int((range_size - 1) / 2)
        else:
            range_start = 1
        if (page_obj.number + int((range_size - 1) / 2) < page_obj.paginator.num_pages):
            is_next_ellipsis = True
            range_end = page_obj.number + int((range_size - 1) / 2)
        else:
            range_end = page_obj.paginator.num_pages
        context['page_obj_md'] = {
            'is_pre_ellipsis' : is_pre_ellipsis,
            'is_next_ellipsis' : is_next_ellipsis,
            'range_start' : range_start,
            'range_end' : range_end,
            'page_range' : range(range_start, range_end + 1, 1),
        }
        return context

def search_in_products(request: HttpRequest):
    return render(request, 'product_module/components/search_filter.html')

def filtering_products_with_price(request: HttpRequest):
    return render(request, 'product_module/components/price_filter.html')

def filtering_products_with_categories(request: HttpRequest):
    return render(request, 'product_module/components/category_filter.html')

class ProductDetails_view(DetailView):
    template_name = 'product_module/product-details_page.html'
    queryset = models.Product_model.objects.filter(is_active=True, is_deleted=False)
    slug_field = 'slug'
    context_object_name = 'product'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('details').prefetch_related(Prefetch(
            'details__creators',
            queryset=User.objects.filter(is_active=True),
            to_attr='pcreators'
        )).prefetch_related(Prefetch(
            'details__pcreators__group_connectors',
            queryset=UserConnectorToUserGroup.objects.filter(
                user_group_id=UserGroup_model.objects.get(title='products_creators').pk
            ),
            to_attr='connector_to_pcreators'
        )).prefetch_related(Prefetch(
            'details__with_features',
            queryset=models.ProductFeature_model.objects.filter(is_active=True),
            to_attr='pwith_features'
        )).prefetch_related(Prefetch(
            'details__without_features',
            queryset=models.ProductFeature_model.objects.filter(is_active=True),
            to_attr='pwithout_features'
        )).select_related('owner').prefetch_related(Prefetch(
            'owner__group_connectors',
            queryset=UserConnectorToUserGroup.objects.filter(
                user_group_id=UserGroup_model.objects.get(title='products_owners').pk
            ),
            to_attr='connector_to_powners'
        )).prefetch_related(Prefetch(
            'tags',
            queryset=models.ProductTag_model.objects.filter(is_active=True),
            to_attr='joined_tags'
        )).prefetch_related(Prefetch(
            'categories',
            queryset=models.ProductCategory_model.objects.filter(is_active=True),
            to_attr='joined_categories'
        ))
        return qs

def product_preview_view(request, slug):
    product = models.Product_model.objects.filter(is_active=True, is_deleted=False, slug=slug).select_related('details').first()
    if not product or not product.details.has_preview:
        return Http404()
    return render(request, 'product_module/product-preview_page.html', context={'slug' : slug,})