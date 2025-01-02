# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static
from two_factor.urls import urlpatterns as two_factor_patterns
from django.conf.urls import handler404, handler500
from customer.views import custom_404, custom_500 

handler404 = custom_404
handler500 = custom_500

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    
    path("account/", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE
    path('', include(two_factor_patterns)),
    path('', include('customer.urls')),
    path('product/', include('products.urls')),

    # Leave `Home.Urls` as last the last line
    path("account/", include("apps.home.urls"))
    
]

if settings.DEBUG:
    urlpatterns += static(settings.LOCAL_MEDIA_URL , document_root=settings.MEDIA_ROOT)