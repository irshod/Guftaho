from rest_framework import serializers
from .models import Poet, Book, Poem


class PoetSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()
    poems_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Poet
        fields = [
            'id', 'name', 'slug', 'birth_date', 'death_date', 
            'biography', 'photo', 'books_count', 'poems_count',
            'created_at', 'updated_at'
        ]
    
    def get_books_count(self, obj):
        return obj.books.count()
    
    def get_poems_count(self, obj):
        return Poem.objects.filter(book__poet=obj).count()


class BookSerializer(serializers.ModelSerializer):
    poet = PoetSerializer(read_only=True)
    poems_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'poet', 'description', 
            'publication_date', 'cover_image', 'poems_count',
            'created_at', 'updated_at'
        ]
    
    def get_poems_count(self, obj):
        return obj.poems.count()


class PoemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    
    class Meta:
        model = Poem
        fields = [
            'id', 'title', 'slug', 'book', 'content', 'order',
            'created_at', 'updated_at'
        ]


class PoemListSerializer(serializers.ModelSerializer):
    """Simplified serializer for poem lists"""
    poet_name = serializers.CharField(source='book.poet.name', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Poem
        fields = [
            'id', 'title', 'slug', 'poet_name', 'book_title', 
            'order', 'created_at'
        ]