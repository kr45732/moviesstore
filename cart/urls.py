
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cart.index'),  # Cart index page
    path('purchase/', views.purchase, name='cart.purchase'),  # Purchase page
    path('clear/', views.clear, name='cart.clear'),  # Clear cart
    path('<int:id>/add/', views.add, name='cart.add'),  # Add item to cart
]