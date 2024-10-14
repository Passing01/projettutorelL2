from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import BuyerRegistrationForm, SellerRegistrationForm, ProductForm
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Cart, Product, Order, Payment, Sale, FAQ, ContactMessage
from django.db.models import Sum
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    order = Order.objects.create(buyer=request.user, product=product, seller=product.seller)
    order.save()
    return redirect('buyer_dashboard')
    

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for product_id, quantity in cart.items():
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        products.append({'product': product, 'quantity': quantity})
        cart_items = cart.items.all()
        total = sum(item.product.price * item.quantity for item in cart_items) 
    return render(request, 'cart.html', {'products': products, 'total': total})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'acheteur':
                return redirect('buyer_dashboard')
            elif user.role == 'vendeur':
                return redirect('seller_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def sales_history(request):
    sales = Sale.objects.filter(seller=request.user)
    return render(request, 'sales_history.html', {'sales': sales})

@login_required
def buyer_dashboard(request):
    products = Product.objects.all()
    return render(request, 'buyer_dashboard.html', {'products': products})


@login_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    total_sales = sum(order.product.price for order in Order.objects.filter(seller=request.user))
    top_selling_products = Order.objects.filter(seller=request.user).values('product__name').annotate(total_sales=Sum('product__price')).order_by('-total_sales')
    return render(request, 'seller_dashboard.html', {'products': products, 'total_sales': total_sales, 'top_selling_products': top_selling_products})

def register_view(request):
    return render(request, 'register.html')

def register_buyer(request):
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = BuyerRegistrationForm()
    return render(request, 'register_buyer.html', {'form': form})

def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SellerRegistrationForm()
    return render(request, 'register_seller.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def order_history(request):
    #orders = Order.objects.filter(product__seller=request.user)
    orders = Order.objects.filter(buyer=request.user) 
    return render(request, 'order_history.html', {'orders': orders})

def payment_history(request):
    payments = Payment.objects.filter(buyer=request.user)
    return render(request, 'payment_history.html', {'payments': payments})

def faq(request):
    return render(request, 'fag.html')

@login_required
def faq_admin(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        FAQ.objects.create(question=question, answer=answer)
        return redirect('faq_admin')  # Remplacez par l'URL de redirection souhaitée

    faqs = FAQ.objects.all()
    return render(request, 'faq_admin.html', {'faqs': faqs})

def contact(request):
    return render(request, 'contact.html')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Associe le vendeur connecté au produit
            product.save()
            return redirect('seller_dashboard')  # Remplacez par l'URL de redirection souhaitée
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})



def payment(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        total = sum(get_object_or_404(Product, id=product_id).price * quantity for product_id, quantity in cart.items())
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),
            currency='usd',
            payment_method_types=['card'],
        )
        return render(request, 'payment.html', {'client_secret': intent.client_secret, 'total': total})
    return redirect('view_cart')

def contact_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Enregistrer le message dans la base de données
        ContactMessage.objects.create(email=email, subject=subject, message=message)
        
        send_mail(
            subject,
            message,
            email,
            ['maverick@example.com'],  # Remplacez par l'email de l'administrateur
        )
        return redirect('home')
    return render(request, 'contact.html')
