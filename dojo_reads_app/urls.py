from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index),
    path('books', views.books),
    path('books/add', views.add_book),
    path('books/<int:book_id>', views.book_details),
    path('users/<int:user_id>', views.user_details),
    path('attempt_login', views.attempt_login),
    path('attempt_reg', views.attempt_reg),
    path('logout', views.logout),
    path('attempt_book', views.attempt_book),
    path('attempt_review', views.attempt_review),
]