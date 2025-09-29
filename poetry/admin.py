from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from django.utils.safestring import mark_safe
from .models import Poet, Book, Poem, Favorite, ReadingHistory


class BookInline(admin.StackedInline):
    model = Book
    extra = 0
    fields = ['title', 'slug', 'description', 'publication_date', 'cover_image', 'is_featured']
    readonly_fields = ['view_count']


class PoemInline(admin.StackedInline):
    model = Poem
    extra = 0
    fields = ['title', 'slug', 'content', 'order', 'is_featured']
    readonly_fields = ['view_count', 'word_count', 'line_count']


@admin.register(Poet)
class PoetAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'birth_date', 'death_date', 'books_count', 
        'poems_count', 'view_count', 'is_featured', 'created_at'
    ]
    list_filter = [
        'is_featured', 'birth_date', 'death_date', 'nationality', 
        'created_at', 'updated_at'
    ]
    search_fields = ['name', 'biography', 'birth_place', 'nationality']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'books_count', 'poems_count']
    inlines = [BookInline]
    
    fieldsets = (
        ('Маълумоти асосӣ', {
            'fields': ('name', 'slug', 'photo', 'is_featured')
        }),
        ('Маълумоти зиндагӣ', {
            'fields': ('birth_date', 'death_date', 'birth_place', 'nationality', 'biography')
        }),
        ('Омор', {
            'fields': ('view_count', 'books_count', 'poems_count'),
            'classes': ('collapse',)
        }),
        ('Санаҳо', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_featured', 'make_unfeatured']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            books_count=Count('books'),
            poems_count=Count('books__poems')
        )

    def books_count(self, obj):
        return obj.books_count
    books_count.short_description = 'Китобҳо'
    books_count.admin_order_field = 'books_count'

    def poems_count(self, obj):
        return obj.poems_count
    poems_count.short_description = 'Шеърҳо'
    poems_count.admin_order_field = 'poems_count'

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} шоир намоён карда шуд.")
    make_featured.short_description = "Намоён кардан"

    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} шоир аз намоён хориҷ карда шуд.")
    make_unfeatured.short_description = "Аз намоён хориҷ кардан"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'poet_link', 'publication_date', 'poems_count', 
        'view_count', 'is_featured', 'created_at'
    ]
    list_filter = [
        'is_featured', 'poet', 'publication_date', 'language', 
        'created_at', 'updated_at'
    ]
    search_fields = ['title', 'description', 'poet__name', 'isbn']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'poems_count']
    inlines = [PoemInline]
    
    fieldsets = (
        ('Маълумоти китоб', {
            'fields': ('title', 'slug', 'poet', 'cover_image', 'is_featured')
        }),
        ('Тавзеҳот', {
            'fields': ('description', 'publication_date', 'isbn', 'page_count', 'language')
        }),
        ('Омор', {
            'fields': ('view_count', 'poems_count'),
            'classes': ('collapse',)
        }),
        ('Санаҳо', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_featured', 'make_unfeatured']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('poet').annotate(
            poems_count=Count('poems')
        )

    def poet_link(self, obj):
        url = reverse('admin:poetry_poet_change', args=[obj.poet.id])
        return format_html('<a href="{}">{}</a>', url, obj.poet.name)
    poet_link.short_description = 'Шоир'
    poet_link.admin_order_field = 'poet__name'

    def poems_count(self, obj):
        return obj.poems_count
    poems_count.short_description = 'Шеърҳо'
    poems_count.admin_order_field = 'poems_count'

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} китоб намоён карда шуд.")
    make_featured.short_description = "Намоён кардан"

    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} китоб аз намоён хориҷ карда шуд.")
    make_unfeatured.short_description = "Аз намоён хориҷ кардан"


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'book_link', 'poet_name', 'order', 'word_count', 
        'line_count', 'view_count', 'difficulty_level', 'is_featured', 'created_at'
    ]
    list_filter = [
        'is_featured', 'book__poet', 'book', 'difficulty_level', 
        'created_at', 'updated_at'
    ]
    search_fields = ['title', 'content', 'book__title', 'book__poet__name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['order', 'difficulty_level']
    readonly_fields = ['view_count', 'word_count', 'line_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Маълумоти шеър', {
            'fields': ('title', 'slug', 'book', 'order', 'is_featured', 'difficulty_level')
        }),
        ('Матни шеър', {
            'fields': ('content',)
        }),
        ('Омор', {
            'fields': ('view_count', 'word_count', 'line_count'),
            'classes': ('collapse',)
        }),
        ('Санаҳо', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_featured', 'make_unfeatured', 'recalculate_stats']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('book__poet')

    def poet_name(self, obj):
        return obj.book.poet.name
    poet_name.short_description = 'Шоир'
    poet_name.admin_order_field = 'book__poet__name'

    def book_link(self, obj):
        url = reverse('admin:poetry_book_change', args=[obj.book.id])
        return format_html('<a href="{}">{}</a>', url, obj.book.title)
    book_link.short_description = 'Китоб'
    book_link.admin_order_field = 'book__title'

    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} шеър намоён карда шуд.")
    make_featured.short_description = "Намоён кардан"

    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} шеър аз намоён хориҷ карда шуд.")
    make_unfeatured.short_description = "Аз намоён хориҷ кардан"

    def recalculate_stats(self, request, queryset):
        for poem in queryset:
            poem.save()  # This will trigger auto-calculation of word_count and line_count
        self.message_user(request, f"Омори {queryset.count()} шеър навсозӣ карда шуд.")
    recalculate_stats.short_description = "Навсозии омор"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']

    def has_add_permission(self, request):
        return False  # Favorites are only created through the frontend


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'poem_title', 'book_title', 'poet_name', 'reading_progress', 'read_at']
    list_filter = ['reading_progress', 'read_at', 'poem__book__poet']
    search_fields = ['user__username', 'poem__title', 'poem__book__title', 'poem__book__poet__name']
    readonly_fields = ['read_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'poem__book__poet')

    def poem_title(self, obj):
        return obj.poem.title
    poem_title.short_description = 'Шеър'
    poem_title.admin_order_field = 'poem__title'

    def book_title(self, obj):
        return obj.poem.book.title
    book_title.short_description = 'Китоб'
    book_title.admin_order_field = 'poem__book__title'

    def poet_name(self, obj):
        return obj.poem.book.poet.name
    poet_name.short_description = 'Шоир'
    poet_name.admin_order_field = 'poem__book__poet__name'

    def has_add_permission(self, request):
        return False  # Reading history is only created through the frontend


# Customize admin site headers
admin.site.site_header = "Гуфтугў - Идоракунии сомона"
admin.site.site_title = "Гуфтугў"
admin.site.index_title = "Пульти идоракунӣ"