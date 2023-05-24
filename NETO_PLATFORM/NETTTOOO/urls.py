from django.urls import path
from . import views


urlpatterns = [
    path('orders/', views.order_view, name='api_order_response'),
    
    path('products/', views.product_info_api, name='product_info_api'),
    # Add more URL patterns as needed
]
