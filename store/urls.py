from django.urls import path
from . import views

urlpatterns = [ # a List of paths
    path('', views.store, name="store"), # empty string is our homepage and dynamic name is store here
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
]