from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse

from .models import MainMenu, Wishlist
from .forms import BookForm, SearchForm
from django.http import HttpResponseRedirect
from .models import Book, Review, Shoppingcart, Order


from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    review = Review.objects.filter(book=book)
    book.pic_path = book.picture.url[14:]
    print(book.name)
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'reviews':review,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    print(book.name)
    return render(request,
                  'bookMng/delete_book.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )
@login_required(login_url=reverse_lazy('login'))
def Review_rate(request):
    if request.method == "GET":
        book_id = request.GET.get('book_id')
        book = Book.objects.get(id=book_id)
        comment = request.GET.get('comment')
        rating = request.GET.get('rating')
        username = request.user
        Review(username=username, book=book, comment=comment, rating=rating).save()
        return redirect('book_detail', book_id)

@login_required(login_url=reverse_lazy('login'))
def searchbook(request):
    if request.method == 'POST':
        form = SearchForm(request.POST, request.FILES)
        name = " "
        if form.is_valid():
            name = form.cleaned_data.get("name")
        return HttpResponseRedirect('/searchresults/' + name)
    else:
        form = SearchForm()
    return render(request,
                  'bookMng/searchbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def searchresults(request, book_name):
    books = Book.objects.filter(name=book_name)
    empty = False
    if books:
        for book in books:
            book.pic_path = book.picture.url[14:]
    else:
        empty = True
    return render(request,
                  'bookMng/searchresults.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'empty': empty
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def wishlist(request):
    empty = False
    try:
        w = Wishlist.objects.get(username=request.user)
        books = w.books.all()
    except Exception:
        empty = True
        books = []
    if books:
        for book in books:
            book.pic_path = book.picture.url[14:]
    else:
        empty = True
    return render(request,
                  'bookMng/wishlist.html',
                  {
                      'books': books,
                      'item_list': MainMenu.objects.all(),
                      'empty': empty
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def wishlist_add(request, book_id):
    book = Book.objects.get(id=book_id)
    try:
        Wishlist.objects.get(username=request.user).books.add(book)
        Wishlist.objects.get(username=request.user).save()
    except Exception:
        w = Wishlist()
        w.username = request.user
        w.save()
        w.books.add(book)
        w.save()
    return render(request,
                  'bookMng/wishlist_add.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def wishlist_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    try:
        Wishlist.objects.get(username=request.user).books.remove(book)
        Wishlist.objects.get(username=request.user).save()
    except Exception:
        w = Wishlist()
        w.username = request.user
        w.save()
        w.books.remove(book)
        w.save()
    return render(request,
                  'bookMng/wishlist_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def shoppingcart(request):
    empty = False
    price = 0
    try:
        s = Shoppingcart.objects.get(username=request.user)
        books = s.books.all()
    except Exception:
        empty = True
        books = []
    if books:
        for book in books:
            book.pic_path = book.picture.url[14:]
            price += book.price
    else:
        empty = True
    return render(request,
                  'bookMng/shoppingcart.html',
                  {
                      'books': books,
                      'item_list': MainMenu.objects.all(),
                      'empty': empty,
                      'price': price,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def shoppingcart_add(request, book_id):
    book = Book.objects.get(id=book_id)
    try:
        Shoppingcart.objects.get(username=request.user).books.add(book)
        Shoppingcart.objects.get(username=request.user).save()
    except Exception:
        s = Shoppingcart()
        s.username = request.user
        s.save()
        s.books.add(book)
        s.save()
    return render(request,
                  'bookMng/shoppingcart_add.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def shoppingcart_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    try:
        Shoppingcart.objects.get(username=request.user).books.remove(book)
        Shoppingcart.objects.get(username=request.user).save()
    except Exception:
        s = Shoppingcart()
        s.username = request.user
        s.save()
        s.books.remove(book)
        s.save()
    return render(request,
                  'bookMng/shoppingcart_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
    )
@login_required
def checkout(request):
    cart = Shoppingcart.objects.filter(username=request.user).first()
    if not cart or cart.books.count() == 0:
        return redirect('displaybooks')

    total_amount = sum([book.price for book in cart.books.all()])
    num_books = cart.books.count()

    if request.method == 'POST':
        # Form handling for checkout information
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        payment_method = request.POST.get('payment')

        # Create the order without passing 'name' since it's not a field in the Order model
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            address=address,
            city=city,
            country=country,
            payment_method=payment_method,
            is_paid=False  # Assume payment happens after this
        )

        # Link the books from the shopping cart to the order
        order.books.set(cart.books.all())

        # Clear the cart after checkout (optional)
        cart.books.clear()

        return redirect('order_confirmation')  # Redirect to order confirmation or payment page

    return render(request, 'bookMng/checkout.html', {'total_amount': total_amount, 'num_books': num_books})


def order_confirmation(request):
    # Retrieve the order ID from the session (if it's available)
    order_id = request.session.get('order_id')

    if not order_id:
        return HttpResponse('No order found', status=404)  # Handle case where order ID is not in session

    try:
        # Fetch the order object from the database
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse('Order not found', status=404)  # Handle case where the order does not exist

    context = {
        'order': order,  # Pass the order object to the template for rendering
    }

    # Render the confirmation page with the order details
    return render(request, 'order_confirmation.html', context)