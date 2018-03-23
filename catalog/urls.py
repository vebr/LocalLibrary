from django.urls import path
from . import views

app_name = 'catalog'
urlpatterns = [
    #catalog index
    path('',views.index,{'foo': 'abc'} ,name='index'),
    #list of all books
    path('books/',views.Books.as_view(), name='books'),
    #list of all authors
    path('authors/',views.Authors.as_view(), name='authors'),
    path('genre/',views.Genres.as_view(), name='genre'),
    path('genre/<int:pk>/',views.GenreDetail.as_view(), name='genre_detail'),
    #detail of specifiec book
    path('books/<int:pk>/',views.BookDetail.as_view(), name='book_detail'),
    #detail of specifiec author
    path('authors/<int:pk>/',views.AuthorDetail.as_view(), name='author_detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my_borrowed'),
    path('borrow-book/<str:pk>/',views.BorrowBook.as_view(),name='borrow_book'),
]