from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Poet, Book, Poem


def home_view(request):
    """Home page listing all poets"""
    poets = Poet.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        poets = poets.filter(
            Q(name__icontains=search_query) |
            Q(biography__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(poets, 12)  # 12 poets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_poets': poets.count(),
    }
    return render(request, 'poetry/home.html', context)


def poet_detail_view(request, slug):
    """Poet detail page showing biography and books"""
    poet = get_object_or_404(Poet, slug=slug)
    books = poet.books.all()
    
    context = {
        'poet': poet,
        'books': books,
    }
    return render(request, 'poetry/poet_detail.html', context)


def book_detail_view(request, slug):
    """Book detail page showing all poems/chapters"""
    book = get_object_or_404(Book, slug=slug)
    poems = book.poems.all()
    
    # Pagination for poems
    paginator = Paginator(poems, 20)  # 20 poems per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'book': book,
        'page_obj': page_obj,
        'total_poems': poems.count(),
    }
    return render(request, 'poetry/book_detail.html', context)


def poem_detail_view(request, book_slug, poem_slug):
    """Individual poem page with navigation"""
    book = get_object_or_404(Book, slug=book_slug)
    poem = get_object_or_404(Poem, book=book, slug=poem_slug)
    
    # Get previous and next poems for navigation
    previous_poem = poem.get_previous_poem()
    next_poem = poem.get_next_poem()
    
    context = {
        'poem': poem,
        'book': book,
        'previous_poem': previous_poem,
        'next_poem': next_poem,
    }
    return render(request, 'poetry/poem_detail.html', context)


def search_view(request):
    """Advanced search functionality"""
    query = request.GET.get('q', '')
    poet_filter = request.GET.get('poet', '')
    book_filter = request.GET.get('book', '')
    
    poems = Poem.objects.all()
    
    if query:
        poems = poems.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(book__title__icontains=query) |
            Q(book__poet__name__icontains=query)
        )
    
    if poet_filter:
        poems = poems.filter(book__poet__slug=poet_filter)
    
    if book_filter:
        poems = poems.filter(book__slug=book_filter)
    
    # Get filters for the form
    poets = Poet.objects.all()
    books = Book.objects.all()
    
    # Pagination
    paginator = Paginator(poems, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'poet_filter': poet_filter,
        'book_filter': book_filter,
        'poets': poets,
        'books': books,
        'total_results': poems.count(),
    }
    return render(request, 'poetry/search.html', context)
