from django.contrib import admin
from django.shortcuts import render
from .models import ContactMessage, CustomUser, Product, Order, Payment, Sale, Cart, CartItem
from django.contrib.auth.decorators import login_required

# Enregistrer le modèle CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')  # Champs à afficher
    list_filter = ('role', 'is_staff', 'is_active')  # Filtrer par rôle et statut
    search_fields = ('username', 'email')  # Champ de recherche
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

# Enregistrer le modèle Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'seller')  # Champs à afficher
    search_fields = ('name', 'description')  # Champ de recherche
    list_filter = ('seller',)  # Filtrer par vendeur

# Enregistrer le modèle Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'seller', 'order_date', 'delivery_status')  # Champs à afficher
    search_fields = ('buyer__username', 'product__name')  # Champ de recherche
    list_filter = ('delivery_status',)  # Filtrer par statut de livraison

# Enregistrer le modèle Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'payment_date', 'amount')  # Champs à afficher
    search_fields = ('buyer__username', 'product__name')  # Champ de recherche

# Enregistrer le modèle Sale
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('seller', 'product', 'sale_date', 'amount')  # Champs à afficher
    search_fields = ('seller__username', 'product__name')  # Champ de recherche

# Enregistrer le modèle Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Champs à afficher
    search_fields = ('user__username',)  # Champ de recherche

# Enregistrer le modèle CartItem
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')  # Champs à afficher
    search_fields = ('cart__user__username', 'product__name')  # Champ de recherche

@login_required
def contact_message_admin(request):
    messages = ContactMessage.objects.all()
    return render(request, 'contact_message_admin.html', {'messages': messages})

