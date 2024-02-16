from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.base import View
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Brand, CartItem, Category
from .forms import ReviewForm
from urllib.parse import unquote


class SearchView(ListView):
    model = Product
    template_name = 'mainprog/product_list.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()

        if query:
            queryset = queryset.filter(title__icontains=query)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context


class SearchViewByPrice(ListView):
    model = Product
    template_name = 'mainprog/product_list2.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = super().get_queryset()

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        brand_slug = self.kwargs.get('slug')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if brand_slug:
            queryset = queryset.filter(brand__url=brand_slug)

        return queryset


class MainView(ListView):
    model = Product
    template_name = 'mainprog/index.html'


class BrandView(ListView):
    model = Brand
    template_name = 'mainprog/companies.html'
    context_object_name = 'brands'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        category = get_object_or_404(Category, url=category_slug)

        queryset = queryset.filter(category=category)
        queryset = queryset.order_by('?')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, url=self.request.GET.get('category'))
        return context


class ViewChoiceProduct(ListView):
    model = Product
    template_name = 'mainprog/tovar.html'
    context_object_name = 'tovar'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        category_slug = self.request.GET.get('category')
        if category_slug:
            category = get_object_or_404(Category, url=category_slug)
            queryset = queryset.filter(category=category)

        brand_slug = self.kwargs.get('slug')
        if brand_slug:
            brand = get_object_or_404(Brand, url=brand_slug)
            queryset = queryset.filter(brand=brand)

        queryset = queryset.order_by('?')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        brand_slug = self.kwargs.get('slug')
        brand = get_object_or_404(Brand, url=brand_slug)

        category_slug = self.request.GET.get('category')
        if category_slug:
            category = get_object_or_404(Category, url=category_slug)
            brand_products = brand.product_brand.filter(category=category)
            context['category'] = category

        else:
            brand_products = brand.product_brand.all()

        context['brand'] = brand
        context['brand_products'] = brand_products

        return context


class BuyView(DetailView):
    model = Product
    slug_field = 'url'
    template_name = 'mainprog/buytovar.html'
    context_object_name = 'view'


class AddReview(View):

    def post(self, request, pk):

        error = ''

        form = ReviewForm(request.POST)
        prod = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.product = prod
            form.save()

        return redirect(prod.get_absolute_url())


class AddToCartView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'mainprog/basket.html'
    context_object_name = 'cart_items'

    def get(self, request, *args, **kwargs):
        product_url = request.GET.get('product_url')
        product_url = unquote(product_url)  # Decode URL if needed
        product = get_object_or_404(Product, url=product_url)

        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return HttpResponseRedirect(reverse('cart'))

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('user')


class CartView(LoginRequiredMixin, ListView):
    template_name = 'mainprog/basket.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = self.get_queryset()
        return context


class RemoveFromCartView(ListView):
    model = CartItem
    template_name = 'mainprog/basket.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        cart_item = get_object_or_404(CartItem, product_id=product_id, user=self.request.user)
        cart_item.delete()
        return CartItem.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        cart_item = get_object_or_404(CartItem, product_id=product_id, user=request.user)
        cart_item.delete()
        return redirect('cart')

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)