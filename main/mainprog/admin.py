from django.contrib import admin
from .models import Product, TypeOfProduct, Category, Brand, Reviews, ProductShots, CartItem


admin.site.register(Product)
admin.site.register(TypeOfProduct)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductShots)
admin.site.register(Reviews)
admin.site.register(CartItem)