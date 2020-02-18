from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# GET for Index page
def index(request):
    return render(request, 'index.html')    

# GET for Books page
def books(request):
    try:
        current_user = User.objects.get(id=request.session['user_id'])
        # separate 'books' into one for first 3 and one for the rest
        context = {
            "first_name":current_user.first_name,
            "books":Book.objects.all()
        }
        return render(request, 'books.html', context)
    except KeyError:
        return redirect('/')

# GET for Add Book page
# TODO add potential author list
def add_book(request):
    try:
        current_user = User.objects.get(id=request.session['user_id'])
        context = {
            "first_name":current_user.first_name
        }
        return render(request, 'books_add.html', context)
    except KeyError:
        return redirect('/')
    
# GET for Book Detail page
def book_details(request, book_id):
    try:
        current_user = User.objects.get(id=request.session['user_id'])
        context = {
            "first_name":current_user.first_name,
            "book":Book.objects.get(id=book_id),
        }
        return render(request, 'book_details.html', context)
    except KeyError:
        return redirect('/')
    
# GET for User Detail page
def user_details(request, user_id):
    try:
        current_user = User.objects.get(id=request.session['user_id'])
        lookup_user = User.objects.get(id=user_id)
        temp_book_list = lookup_user.reviews.all().values('book').distinct()
        book_list = []
        for book in temp_book_list:
            book_list.append(Book.objects.get(id=book['book']))
            
        context = {
            "name":lookup_user.first_name + " " + lookup_user.last_name,
            "email":lookup_user.email,
            "review_len":len(lookup_user.reviews.all()),
            "book_list":book_list,
        }
        return render(request, 'user_details.html', context)
    except KeyError:
        return redirect('/')

# POST for attempting to log in, if successful, route to books
def attempt_login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')    
    
    else:
        current_user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = current_user.id
        return redirect('/books')

# POST for attempting to register, if successful, register and route to books
def attempt_reg(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')    
    
    else:
        # Hashing PW
        pw_hash= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        # Creates new User
        User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            birthdate=request.POST["birthdate"],
            password=pw_hash,
        )
    return redirect('/books')

# POST for logging out, clearing session
def logout(request):
    del request.session['user_id']
    return redirect('/')


# POST for attempting to add book, save and route to books if OK
def attempt_book(request):    
    # Creates new Book
    Book.objects.create(
        title=request.POST["title"],
        author=request.POST["author"],
    )
    # Creates new Review
    Review.objects.create(
        text=request.POST["review_text"],
        rating=request.POST["review_rating"],
        book = Book.objects.last(),
        user=User.objects.get(id=request.session['user_id']),
    )
    
    return redirect(f'/books/{Book.objects.last().id}')

# POST for attempting to add review, save and route to reviews if OK
def attempt_review(request):
    # Creates new Review
    Review.objects.create(
        text=request.POST["review_text"],
        rating=request.POST["review_rating"],
        book = Book.objects.get(id=request.POST["book_id"]),
        user=User.objects.get(id=request.session['user_id']),
    )
    
    return redirect(f'/books/{Book.objects.get(id=request.POST["book_id"]).id}')