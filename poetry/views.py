from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count, Prefetch, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.conf import settings
from .models import Poet, Book, Poem, Favorite, ReadingHistory
from .filters import PoetFilter, BookFilter, PoemFilter, AdvancedSearchFilter
import json


class HomeView(ListView):
    """Enhanced home page with featured content"""
    model = Poet
    template_name = 'poetry/home.html'
    context_object_name = 'poets'
    paginate_by = 12

    def get_queryset(self):
        queryset = Poet.objects.with_stats()
        
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(biography__icontains=search_query)
            )
        
        return queryset.order_by('-is_featured', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_query': self.request.GET.get('search', ''),
            'featured_poets': Poet.objects.featured()[:6],
            'recent_books': Book.objects.recent(6),
            'featured_poems': Poem.objects.featured()[:8],
            'total_poets': Poet.objects.count(),
            'total_books': Book.objects.count(),
            'total_poems': Poem.objects.count(),
        })
        return context


home_view = HomeView.as_view()


class PoetDetailView(DetailView):
    """Enhanced poet detail view"""
    model = Poet
    template_name = 'poetry/poet_detail.html'
    context_object_name = 'poet'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Poet.objects.prefetch_related(
            Prefetch('books', queryset=Book.objects.order_by('-publication_date'))
        )

    def get_object(self):
        obj = super().get_object()
        # Increment view count
        obj.increment_view_count()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poet = self.object
        
        # Get books with poem counts
        books = poet.books.annotate(poems_count=Count('poems')).order_by('-publication_date')
        
        # Pagination for books
        paginator = Paginator(books, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'books': page_obj,
            'total_books': books.count(),
            'total_poems': Poem.objects.filter(book__poet=poet).count(),
            'recent_poems': Poem.objects.filter(book__poet=poet)[:5],
        })
        
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(
                user=self.request.user,
                content_type='poet',
                object_id=poet.id
            ).exists()
        
        return context


poet_detail_view = PoetDetailView.as_view()


class BookDetailView(DetailView):
    """Enhanced book detail view"""
    model = Book
    template_name = 'poetry/book_detail.html'
    context_object_name = 'book'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Book.objects.select_related('poet').prefetch_related('poems')

    def get_object(self):
        obj = super().get_object()
        # Increment view count
        obj.increment_view_count()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        
        poems = book.poems.all()
        
        # Pagination for poems
        paginator = Paginator(poems, getattr(settings, 'PAGINATION_SETTINGS', {}).get('POEMS_PER_PAGE', 20))
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'poems': page_obj,
            'page_obj': page_obj,
            'total_poems': poems.count(),
        })
        
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(
                user=self.request.user,
                content_type='book',
                object_id=book.id
            ).exists()
            
            # Get reading progress
            read_poems = ReadingHistory.objects.filter(
                user=self.request.user,
                poem__book=book
            ).count()
            context['reading_progress'] = (read_poems / poems.count() * 100) if poems.count() > 0 else 0
        
        return context


book_detail_view = BookDetailView.as_view()


class PoemDetailView(DetailView):
    """Enhanced poem detail view"""
    model = Poem
    template_name = 'poetry/poem_detail.html'
    context_object_name = 'poem'

    def get_object(self):
        book_slug = self.kwargs.get('book_slug')
        poem_slug = self.kwargs.get('poem_slug') or self.kwargs.get('slug')
        
        if book_slug:
            # Full URL pattern with book
            book = get_object_or_404(Book, slug=book_slug)
            poem = get_object_or_404(Poem, book=book, slug=poem_slug)
        else:
            # Simple URL pattern with just poem slug
            poem = get_object_or_404(Poem, slug=poem_slug)
        
        # Increment view count
        poem.increment_view_count()
        
        # Track reading history for authenticated users
        if self.request.user.is_authenticated:
            ReadingHistory.objects.update_or_create(
                user=self.request.user,
                poem=poem,
                defaults={'reading_progress': 100}
            )
        
        return poem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poem = self.object
        
        # Get previous and next poems for navigation
        previous_poem = poem.get_previous_poem()
        next_poem = poem.get_next_poem()
        
        context.update({
            'book': poem.book,
            'previous_poem': previous_poem,
            'next_poem': next_poem,
        })
        
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(
                user=self.request.user,
                content_type='poem',
                object_id=poem.id
            ).exists()
        
        return context


poem_detail_view = PoemDetailView.as_view()


class AdvancedSearchView(ListView):
    """Enhanced search with multiple filters"""
    template_name = 'poetry/search.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        self.query = self.request.GET.get('q', '')
        self.poet_filter = self.request.GET.get('poet', '')
        self.book_filter = self.request.GET.get('book', '')
        
        queryset = Poem.objects.select_related('book__poet').all()
        
        # Apply search filters
        if self.query:
            queryset = queryset.filter(
                Q(title__icontains=self.query) |
                Q(content__icontains=self.query)
            )
        
        if self.poet_filter:
            queryset = queryset.filter(book__poet__slug=self.poet_filter)
        
        if self.book_filter:
            queryset = queryset.filter(book__slug=self.book_filter)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add all poets and books for filter dropdowns
        context.update({
            'query': self.query,
            'poet_filter': self.poet_filter,
            'book_filter': self.book_filter,
            'poets': Poet.objects.all().order_by('name'),
            'books': Book.objects.select_related('poet').all().order_by('title'),
        })
        return context


search_view = AdvancedSearchView.as_view()


@login_required
@require_http_methods(["POST"])
def toggle_favorite(request):
    """Toggle favorite status for poems, books, or poets"""
    content_type = request.POST.get('content_type')
    object_id = request.POST.get('object_id')
    
    if not content_type or not object_id:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    try:
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=int(object_id)
        )
        
        if not created:
            favorite.delete()
            is_favorited = False
        else:
            is_favorited = True
        
        return JsonResponse({
            'is_favorited': is_favorited,
            'message': 'Ба дӯстдоштаҳо илова шуд' if is_favorited else 'Аз дӯстдоштаҳо хориҷ шуд'
        })
    
    except ValueError:
        return JsonResponse({'error': 'Invalid object ID'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def favorites_view(request):
    """User's favorites page"""
    favorite_poets = []
    favorite_books = []
    favorite_poems = []
    
    favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
    
    for fav in favorites:
        if fav.content_type == 'poet':
            try:
                poet = Poet.objects.get(id=fav.object_id)
                favorite_poets.append(poet)
            except Poet.DoesNotExist:
                pass
        elif fav.content_type == 'book':
            try:
                book = Book.objects.select_related('poet').get(id=fav.object_id)
                favorite_books.append(book)
            except Book.DoesNotExist:
                pass
        elif fav.content_type == 'poem':
            try:
                poem = Poem.objects.select_related('book__poet').get(id=fav.object_id)
                favorite_poems.append(poem)
            except Poem.DoesNotExist:
                pass
    
    context = {
        'favorite_poets': favorite_poets,
        'favorite_books': favorite_books,
        'favorite_poems': favorite_poems,
    }
    
    return render(request, 'poetry/favorites.html', context)


@login_required
def reading_history_view(request):
    """User's reading history"""
    history = ReadingHistory.objects.filter(user=request.user).select_related(
        'poem__book__poet'
    ).order_by('-read_at')
    
    paginator = Paginator(history, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_read': history.count(),
    }
    
    return render(request, 'poetry/reading_history.html', context)


@cache_page(60 * 15)  # Cache for 15 minutes
def statistics_view(request):
    """Site statistics page"""
    stats = {
        'total_poets': Poet.objects.count(),
        'total_books': Book.objects.count(),
        'total_poems': Poem.objects.count(),
        'total_views': (
            (Poet.objects.aggregate(total=Sum('view_count'))['total'] or 0) +
            (Book.objects.aggregate(total=Sum('view_count'))['total'] or 0) +
            (Poem.objects.aggregate(total=Sum('view_count'))['total'] or 0)
        ),
        'most_viewed_poets': Poet.objects.order_by('-view_count')[:10],
        'most_viewed_books': Book.objects.select_related('poet').order_by('-view_count')[:10],
        'most_viewed_poems': Poem.objects.select_related('book__poet').order_by('-view_count')[:10],
        'recent_additions': {
            'poets': Poet.objects.order_by('-created_at')[:5],
            'books': Book.objects.select_related('poet').order_by('-created_at')[:5],
            'poems': Poem.objects.select_related('book__poet').order_by('-created_at')[:5],
        }
    }
    
    return render(request, 'poetry/statistics.html', {'stats': stats})