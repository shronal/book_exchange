from django import forms
from django.forms import ModelForm, CharField, URLField, DecimalField, FileField
from .models import Book, Search

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]

class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = [
            'name'
        ]



class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Shipping Address'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    payment_method = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])

class CheckoutForm(forms.Form):
    # Form fields for checkout process
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Shipping Address'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    payment_method = forms.ChoiceField(
        choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')],
        widget=forms.RadioSelect,  # Display as radio buttons
    )