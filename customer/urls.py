
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
# from django.conf.urls import handler404, handler500

# handler404 = views.custom_404
# handler500 = views.custom_500

urlpatterns = [
    path('', views.customer_home, name='customer_home'),
    # path('product/', views.product_list, name='product_list'),
    path('custom-register/', views.customer_register, name='customer_register'),
    path('custom-login/', views.customer_login, name='customer_login'),
    path('custom-logout/', views.custom_logout, name='logout'),
    path('custom-profile/', views.customer_profile, name='customer_profile'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('schedule-demo/', views.schedule_demo, name='schedule_demo'),
    path('subscribe/', views.subscribe, name='subscribe'),
    
    # path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('download/<int:purchase_id>/', views.purchase_success, name='purchase_success'),
    path('download-file/<int:purchase_id>/', views.download_file, name='download_file'),
    
    # Password Reset Views
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='customer-temp/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='customer-temp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='customer-temp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='customer-temp/password_reset_complete.html'), name='password_reset_complete'),
    
    # Mail verification Views
    # path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate_account'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
]
