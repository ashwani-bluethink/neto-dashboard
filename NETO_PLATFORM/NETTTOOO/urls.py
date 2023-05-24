from django.urls import path
from .views import order_view,Fiter_order_view,index

urlpatterns = [
    path('Orders/', order_view, name='order_view'),
    path('Fiter_Orders/', Fiter_order_view, name='Fiter_order_view'),\
]