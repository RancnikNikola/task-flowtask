"""zadatak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import register
from django.contrib.auth import views as auth_view
from .views import OrderListView, OrderCreateView, OrderDetailView, OrderUpdateView, load_models


urlpatterns = [
    path('register/', register, name="register"),
    path('login/', auth_view.LoginView.as_view(template_name="kodius/login.html"), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name="kodius/logout.html"), name="logout"),
    path('my_orders/', OrderListView.as_view(template_name="kodius/my_orders.html"), name="my_orders"),
    path('new_order/', OrderCreateView.as_view(), name="new_order"),
    path('my_orders/<int:pk>/', OrderDetailView.as_view(template_name="kodius/order_details.html"), name="order_details"),
    path('my_orders/<int:pk>/update', OrderUpdateView.as_view(),
         name="order_update"),


    path('ajax/load-models/', load_models, name="ajax_load_models")
]