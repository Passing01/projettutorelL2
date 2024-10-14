from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, User

class CustomUser(AbstractUser):
    role = models.CharField(max_length=255)
    ROLE_CHOICES = (
        ('acheteur', 'Acheteur'),
        ('vendeur', 'Vendeur'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='acheteur')
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Order(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales', default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=50, default='En cours')

    def __str__(self):
        return f"Order {self.id} by {self.buyer.username}"

class Payment(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.id} by {self.buyer.username}"

class Sale(models.Model):
    seller = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale {self.id} by {self.seller.username}"

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class ContactMessage(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.email} - {self.subject}"

