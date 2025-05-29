from django.db import models

# Create your models here.

from django.contrib.auth.models import User



class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Review(models.Model):
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, models.CASCADE)
    comment = models.TextField(max_length=500)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Search(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Wishlist(models.Model):
    books = models.ManyToManyField(Book)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username)


class Shoppingcart(models.Model):
    books = models.ManyToManyField(Book)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username)

        from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import FormView
from .models import Shoppingcart, Book
from .forms import CheckoutForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Book  # Assuming you have a Book model

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who placed the order
    name = models.CharField(max_length=200, default=True)  # Store the user's name
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total price of the order
    address = models.TextField()  # Shipping address
    city = models.CharField(max_length=100)  # City
    country = models.CharField(max_length=100)  # Country
    payment_method = models.CharField(max_length=100)  # Payment method (e.g., credit card, PayPal)
    is_paid = models.BooleanField(default=False)  # Whether the order is paid or not
    created_at = models.DateTimeField(auto_now_add=True)  # Order creation date
    updated_at = models.DateTimeField(auto_now=True)  # Last update date
    books = models.ManyToManyField(Book)  # List of books in the order

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    def get_total_amount(self):
        """Method to calculate the total price of books in the order"""
        return sum([book.price for book in self.books.all()])

class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'checkout.html'
    form_class = CheckoutForm  # Using the form defined above

    def get_context_data(self, **kwargs):
        # Get the user's shopping cart
        cart = Shoppingcart.objects.filter(username=self.request.user).first()
        
        # Calculate total amount and number of books in the cart
        if cart:
            total_amount = sum([book.price for book in cart.books.all()])
            num_books = cart.books.count()
        else:
            total_amount = 0
            num_books = 0

        context = super().get_context_data(**kwargs)
        context['total_amount'] = total_amount
        context['num_books'] = num_books
        return context

    def form_valid(self, form):
        from .models import Order
        # Get the user's shopping cart
        cart = Shoppingcart.objects.filter(username=self.request.user).first()
        
        if not cart or cart.books.count() == 0:
            # If no cart or empty cart, redirect to display books
            return redirect('displaybooks')

        # Get form data
        name = form.cleaned_data['name']
        address = form.cleaned_data['address']
        city = form.cleaned_data['city']
        country = form.cleaned_data['country']
        payment_method = form.cleaned_data['payment_method']

        # Calculate total amount from the cart
        total_amount = sum([book.price for book in cart.books.all()])

        # Crea

        order = Order.objects.create(
            user=self.request.user,
            total_amount=total_amount,
            name=name,
            address=address,
            city=city,
            country=country,
            payment_method=payment_method,
            is_paid=False  # Assuming payment happens later
        )
        # Link the books from the shopping cart to the order
        order.books.set(cart.books.all())

        # Clear the shopping cart after order is placed (optional)
        cart.books.clear()

        # Redirect to order confirmation or payment page
        return redirect('order_confirmation')  # You can adjust the redirect here

    def form_invalid(self, form):
        # If the form is invalid, just render the page again with the form errors
        return self.render_to_response(self.get_context_data(form=form))

from django.views.generic import TemplateView



class OrderConfirmationView(TemplateView):
    template_name = 'order_confirmation.html'

    def get_context_data(self, **kwargs):
        # You can pass order details to the template if needed
        order_id = self.request.session.get('order_id')  # Assuming you store the order ID in the session
        context = super().get_context_data(**kwargs)
        context['order_id'] = order_id
        return context
