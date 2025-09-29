from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
import re


def custom_slugify(value):
    """Custom slugify function that handles Persian/Tajik characters better"""
    if not value:
        return ''
    
    value = str(value)
    
    # Tajik Cyrillic and Persian to Latin transliteration map
    char_map = {
        # Tajik Cyrillic to Latin
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'ғ': 'gh', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'ӣ': 'i', 'й': 'y', 'к': 'k', 'қ': 'q', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ӯ': 'u', 'ф': 'f', 'х': 'kh',
        'ҳ': 'h', 'ч': 'ch', 'ҷ': 'j', 'ш': 'sh', 'ъ': '', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        
        # Persian/Arabic to Latin (for backward compatibility)
        'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's', 'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh',
        'د': 'd', 'ذ': 'z', 'ر': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'd',
        'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'q', 'ک': 'k', 'گ': 'g', 'ل': 'l',
        'م': 'm', 'ن': 'n', 'و': 'v', 'ه': 'h', 'ی': 'y', 'ء': '', 'آ': 'a', 'أ': 'a', 'إ': 'e',
        'ة': 'h', 'ى': 'a', 'ئ': 'y', 'ؤ': 'v'
    }
    
    # Replace characters with Latin equivalents
    for char, latin in char_map.items():
        value = value.replace(char, latin)
    
    # Use Django's slugify for the rest
    slug = slugify(value)
    
    # If still empty after slugify, create a fallback
    if not slug:
        # Remove non-alphanumeric characters and create basic slug
        slug = re.sub(r'[^\w\s-]', '', value).strip().lower()
        slug = re.sub(r'[-\s]+', '-', slug)
        if not slug:
            slug = 'item'  # fallback
    
    return slug


class PoetManager(models.Manager):
    def with_stats(self):
        """Get poets with book and poem counts"""
        return self.annotate(
            books_count=models.Count('books'),
            poems_count=models.Count('books__poems')
        )

    def featured(self):
        """Get featured poets (those with most books)"""
        return self.with_stats().filter(books_count__gt=0).order_by('-books_count')[:6]


class Poet(models.Model):
    name = models.CharField(max_length=200, verbose_name="Ном", db_index=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name="Санаи таваллуд")
    death_date = models.DateField(null=True, blank=True, verbose_name="Санаи вафот")
    biography = models.TextField(verbose_name="Таржумаи ҳол")
    photo = models.ImageField(upload_to='poets/', null=True, blank=True, verbose_name="Акс")
    birth_place = models.CharField(max_length=200, blank=True, verbose_name="Ҷои таваллуд")
    nationality = models.CharField(max_length=100, blank=True, verbose_name="Миллият")
    is_featured = models.BooleanField(default=False, verbose_name="Намоён кардан")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Шумораи бозид")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = PoetManager()
    tags = TaggableManager(blank=True, verbose_name="Нишонаҳо")

    class Meta:
        verbose_name = "Шоир"
        verbose_name_plural = "Шоирон"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['birth_date']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.name)
            # Ensure uniqueness
            if self.__class__.objects.filter(slug=self.slug).exists():
                counter = 1
                new_slug = f"{self.slug}-{counter}"
                while self.__class__.objects.filter(slug=new_slug).exists():
                    counter += 1
                    new_slug = f"{self.slug}-{counter}"
                self.slug = new_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('poet_detail', kwargs={'slug': self.slug})

    @property
    def age_at_death(self):
        """Calculate age at death if both dates are available"""
        if self.birth_date and self.death_date:
            return self.death_date.year - self.birth_date.year
        return None

    @property
    def is_alive(self):
        """Check if poet is still alive"""
        return self.death_date is None

    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class BookManager(models.Manager):
    def published(self):
        """Get published books"""
        return self.filter(publication_date__isnull=False)

    def recent(self, limit=10):
        """Get recently added books"""
        return self.order_by('-created_at')[:limit]


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Унвон", db_index=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    poet = models.ForeignKey(Poet, on_delete=models.CASCADE, related_name='books', verbose_name="Шоир")
    description = models.TextField(blank=True, verbose_name="Тавзеҳ")
    publication_date = models.DateField(null=True, blank=True, verbose_name="Санаи нашр")
    cover_image = models.ImageField(upload_to='books/', null=True, blank=True, verbose_name="Акси рӯи китоб")
    isbn = models.CharField(max_length=13, blank=True, verbose_name="ISBN")
    page_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Шумораи саҳифаҳо")
    language = models.CharField(max_length=50, default='Тоҷикӣ', verbose_name="Забон")
    is_featured = models.BooleanField(default=False, verbose_name="Намоён кардан")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Шумораи бозид")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = BookManager()
    tags = TaggableManager(blank=True, verbose_name="Нишонаҳо")

    class Meta:
        verbose_name = "Китоб"
        verbose_name_plural = "Китобҳо"
        ordering = ['-publication_date', 'title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['publication_date']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return f"{self.title} - {self.poet.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.title)
            # Ensure uniqueness
            if self.__class__.objects.filter(slug=self.slug).exists():
                counter = 1
                new_slug = f"{self.slug}-{counter}"
                while self.__class__.objects.filter(slug=new_slug).exists():
                    counter += 1
                    new_slug = f"{self.slug}-{counter}"
                self.slug = new_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})

    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    # @property
    # def poems_count(self):
    #     """Get total number of poems in this book"""
    #     return self.poems.count()


class PoemManager(models.Manager):
    def published(self):
        """Get poems from published books"""
        return self.filter(book__publication_date__isnull=False)

    def featured(self):
        """Get featured poems"""
        return self.filter(is_featured=True)

    def by_poet(self, poet):
        """Get all poems by a specific poet"""
        return self.filter(book__poet=poet)


class Poem(models.Model):
    title = models.CharField(max_length=200, verbose_name="Унвон", db_index=True)
    slug = models.SlugField(blank=True, db_index=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='poems', verbose_name="Китоб")
    content = models.TextField(verbose_name="Матн")
    order = models.PositiveIntegerField(default=0, verbose_name="Тартиб")
    is_featured = models.BooleanField(default=False, verbose_name="Намоён кардан")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Шумораи бозид")
    word_count = models.PositiveIntegerField(default=0, verbose_name="Шумораи калимаҳо")
    line_count = models.PositiveIntegerField(default=0, verbose_name="Шумораи сатрҳо")
    difficulty_level = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Дараҷаи душворӣ"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = PoemManager()
    tags = TaggableManager(blank=True, verbose_name="Нишонаҳо")

    class Meta:
        verbose_name = "Шеър"
        verbose_name_plural = "Шеърҳо"
        ordering = ['order', 'title']
        unique_together = ['book', 'slug']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['order']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['book', 'order']),
        ]

    def __str__(self):
        return f"{self.title} - {self.book.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.title)
            # Ensure uniqueness within the same book
            if self.__class__.objects.filter(book=self.book, slug=self.slug).exists():
                counter = 1
                new_slug = f"{self.slug}-{counter}"
                while self.__class__.objects.filter(book=self.book, slug=new_slug).exists():
                    counter += 1
                    new_slug = f"{self.slug}-{counter}"
                self.slug = new_slug
        
        # Auto-calculate word and line counts
        if self.content:
            self.word_count = len(self.content.split())
            self.line_count = len([line for line in self.content.split('\n') if line.strip()])
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('poem_detail', kwargs={'book_slug': self.book.slug, 'poem_slug': self.slug})

    def get_previous_poem(self):
        return self.book.poems.filter(order__lt=self.order).last()

    def get_next_poem(self):
        return self.book.poems.filter(order__gt=self.order).first()

    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    @property
    def reading_time(self):
        """Estimate reading time in minutes (average 200 words per minute)"""
        if self.word_count > 0:
            return max(1, round(self.word_count / 200))
        return 1


class Favorite(models.Model):
    """User favorites for poems, books, and poets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    content_type = models.CharField(max_length=20, choices=[
        ('poet', 'Шоир'),
        ('book', 'Китоб'),
        ('poem', 'Шеър'),
    ])
    object_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
        verbose_name = "Дӯстдоштаи корбар"
        verbose_name_plural = "Дӯстдоштаҳои корбарон"

    def __str__(self):
        return f"{self.user.username} - {self.content_type} #{self.object_id}"


class ReadingHistory(models.Model):
    """Track user reading history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_history')
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)
    reading_progress = models.PositiveIntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Пешравии хондан (%)"
    )

    class Meta:
        unique_together = ['user', 'poem']
        ordering = ['-read_at']
        verbose_name = "Таърихи хондан"
        verbose_name_plural = "Таърихи хондан"

    def __str__(self):
        return f"{self.user.username} - {self.poem.title}"
