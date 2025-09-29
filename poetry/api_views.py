from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Poet, Book, Poem
from .serializers import PoetSerializer, BookSerializer, PoemSerializer, PoemListSerializer
from .filters import PoetFilter, BookFilter, PoemFilter


class PoetViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for poets"""
    queryset = Poet.objects.all().annotate(
        books_count=Count('books'),
        poems_count=Count('books__poems')
    )
    serializer_class = PoetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PoetFilter
    search_fields = ['name', 'biography']
    ordering_fields = ['name', 'birth_date', 'created_at']
    ordering = ['name']
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def books(self, request, slug=None):
        """Get all books by a specific poet"""
        poet = self.get_object()
        books = poet.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def poems(self, request, slug=None):
        """Get all poems by a specific poet"""
        poet = self.get_object()
        poems = Poem.objects.filter(book__poet=poet)
        serializer = PoemListSerializer(poems, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for books"""
    queryset = Book.objects.select_related('poet').annotate(
        poems_count=Count('poems')
    )
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'description', 'poet__name']
    ordering_fields = ['title', 'publication_date', 'created_at']
    ordering = ['-publication_date']
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def poems(self, request, slug=None):
        """Get all poems in a specific book"""
        book = self.get_object()
        poems = book.poems.all()
        serializer = PoemSerializer(poems, many=True)
        return Response(serializer.data)


class PoemViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for poems"""
    queryset = Poem.objects.select_related('book__poet')
    serializer_class = PoemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PoemFilter
    search_fields = ['title', 'content', 'book__title', 'book__poet__name']
    ordering_fields = ['title', 'order', 'created_at']
    ordering = ['order']

    def get_serializer_class(self):
        if self.action == 'list':
            return PoemListSerializer
        return PoemSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search across all poems"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'results': []})

        poems = self.queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(book__title__icontains=query) |
            Q(book__poet__name__icontains=query)
        )
        
        page = self.paginate_queryset(poems)
        if page is not None:
            serializer = PoemListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PoemListSerializer(poems, many=True)
        return Response(serializer.data)