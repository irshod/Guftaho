from django.contrib import admin
from .models import Poet, Book, Poem


class BookInline(admin.StackedInline):
    model = Book
    extra = 0
    fields = ['title', 'description', 'publication_date', 'cover_image']


class PoemInline(admin.StackedInline):
    model = Poem
    extra = 0
    fields = ['title', 'content', 'order']


@admin.register(Poet)
class PoetAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'death_date', 'created_at']
    list_filter = ['birth_date', 'death_date']
    search_fields = ['name', 'biography']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BookInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'photo')
        }),
        ('اطلاعات زندگی', {
            'fields': ('birth_date', 'death_date', 'biography')
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'poet', 'publication_date', 'created_at']
    list_filter = ['poet', 'publication_date']
    search_fields = ['title', 'description', 'poet__name']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PoemInline]
    
    fieldsets = (
        ('اطلاعات کتاب', {
            'fields': ('title', 'slug', 'poet', 'cover_image')
        }),
        ('توضیحات', {
            'fields': ('description', 'publication_date')
        }),
    )


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'poet_name', 'order', 'created_at']
    list_filter = ['book__poet', 'book']
    search_fields = ['title', 'content', 'book__title', 'book__poet__name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['order']
    
    def poet_name(self, obj):
        return obj.book.poet.name
    poet_name.short_description = 'شاعر'
    
    fieldsets = (
        ('اطلاعات شعر', {
            'fields': ('title', 'slug', 'book', 'order')
        }),
        ('متن شعر', {
            'fields': ('content',)
        }),
    )
