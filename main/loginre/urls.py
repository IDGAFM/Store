from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('logout/', views.logout_view, name='logout'),

        ]
