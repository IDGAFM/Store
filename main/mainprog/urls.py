from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('loginre.urls')),

    path('', views.MainView.as_view(), name="home"),

    path('search/', views.SearchView.as_view(), name='search'),
    path('search1/', views.SearchViewByPrice.as_view(), name='search2'),
    path('add-to-cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path("brands/", views.BrandView.as_view(), name="brand"),


    path("<slug:slug>/", views.ViewChoiceProduct.as_view(), name="view_prod"),

    path("buy/<slug:slug>/", views.BuyView.as_view(), name="buy"),


    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
