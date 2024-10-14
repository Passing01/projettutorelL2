from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, Product
from django.contrib.auth import get_user_model


User = get_user_model()


class BuyerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'gender', 'phone_number', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'acheteur'
        if commit:
            user.save()
        return user


class SellerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    profile_picture = forms.ImageField(required=False)
    profile_type = forms.ChoiceField(choices=[('artisan', 'Artisan'), ('agriculteur', 'Agriculteur')])

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'gender', 'phone_number', 'email', 'profile_picture', 'profile_type', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'vendeur'
        if commit:
            user.save()
        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
