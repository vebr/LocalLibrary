from django.shortcuts import render, get_object_or_404
from django.http import request, Http404
from .models import Author, Genre, Book, Language, BookInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from .forms import BorrowForm
from datetime import datetime

def index(request,foo):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    genree=Genre.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'catalog/index.html',
        context={'genree':genree,'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,
            'num_visits':num_visits}, # num_visits appended
    )

class Books(generic.ListView):
	model = Book
	paginate_by = 5
	context_object_name = 'book_list'
	def get_queryset(self):
		return Book.objects.all()
	
	template_name = 'catalog/book_list.html'

class BookDetail(generic.DetailView):
	model = Book

	def book_detail_view(request,pk):
		try:
			book_id=Book.objects.get(pk=pk)
		except Book.DoesNotExist:
			raise Http404("Book does not exist")

		#book_id=get_object_or_404(Book, pk=pk)

		return render(
			request,
			'catalog/book_detail.html',
		)

class Authors(generic.ListView):
	model = Author
	def get_queryset(self):
		return Author.objects.all()
	
	context_object_name = 'author_list'
	template_name = 'catalog/author_list.html'

class AuthorDetail(generic.DetailView):
	model = Author
	foo=None
	def author_detail_view(self,request,pk):
		globvar = self.pk
		return render(
			request,
			'catalog/author_detail.html',
			)

	def get_context_data(self, **kwargs):
		b = self.kwargs.get('pk')
		context = super(AuthorDetail,self).get_context_data(**kwargs)
		context['book'] = Book.objects.filter(author=b).all()
		return context

class Genres(generic.ListView):
	model = Author
	def get_queryset(self):
		return Genre.objects.all()
	template_name = 'catalog/genre_list.html'

class GenreDetail(generic.DetailView):
	model = Genre
	def genre_detail_view(request,pk):
		try:
			genre_id=Genre.objects.get(pk=pk)
		except Genre.DoesNotExist:
			raise Http404("Genre does not exist")

		return render(
			request,
			'catalog/genre_detail.html',
			)

	def get_context_data(self, **kwargs):
		b = self.kwargs.get('pk')
		context = super(GenreDetail,self).get_context_data(**kwargs)
		context['book'] = Book.objects.filter(genre=b).all()
		return context


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class BorrowBook(LoginRequiredMixin,generic.UpdateView):
	model = BookInstance
	template_name = 'catalog/borrow_book.html'
	form_class = BorrowForm
	def get_context_data(self, **kwargs):
		idb = self.kwargs.get('pk')
		context = super(BorrowBook,self).get_context_data(**kwargs)
		context['book'] = BookInstance.objects.get(id=str(idb))
		return context
	def form_valid(self, form):
		if 'status' != 'a':
			form.instance.borrower = self.request.user
			return super().form_valid(form)
		else:
			form.instance.borrower = ''
			return super().form_valid(form)
