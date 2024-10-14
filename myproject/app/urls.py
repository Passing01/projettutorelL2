from django.urls import path

from .admin import contact_message_admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import faq_admin, contact_view

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('register_buyer/', views.register_buyer, name='register_buyer'),
    path('register_seller/', views.register_seller, name='register_seller'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_detail/<int:id>/', views.product_detail, name='product_detail'),
    path('order_history/', views.order_history, name='order_history'),
    path('payment_history/', views.payment_history, name='payment_history'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('add_product/', views.add_product, name='add_product'),
    path('sales_history/', views.sales_history, name='sales_history'),
    path('payment/', views.payment, name='payment'),
    path('logout/', views.logout_view, name='logout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buyer_dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('admin/faq/', faq_admin, name='faq_admin'),
    path('contact/', contact_view, name='contact'),
    path('admin/contact-messages/', contact_message_admin, name='contact_message_admin'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
