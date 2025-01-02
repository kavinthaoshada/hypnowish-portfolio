
from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:id>/', views.product_detail, name='product_detail'), 
    # path('view-demo/<int:product_id>/<path:screenshot_path>/', views.serve_demo_file, name='view_demo_file'),
    path('view-demo/<int:product_id>/', views.serve_demo_file, name='view_demo_file'),
    path('product/detail/<int:pk>/', views.single_product_detail, name='single_product_detail'),
]
