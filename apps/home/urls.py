# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('admin-home/', views.index, name='home'),
    path('manage_products/', views.manage_product, name='manage-product'),
    path('add-product/', views.add_product, name='add_product'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
