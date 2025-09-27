from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Poet(models.Model):
    name = models.CharField(max_length=200, verbose_name="Ном")
    slug = models.SlugField(unique=True, blank=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name="Санаи таваллуд")
    death_date = models.DateField(null=True, blank=True, verbose_name="Санаи вафот")
    biography = models.TextField(verbose_name="Таржумаи ҳол")
    photo = models.ImageField(upload_to='poets/', null=True, blank=True, verbose_name="Акс")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Шоир"
        verbose_name_plural = "Шоирон"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('poet_detail', kwargs={'slug': self.slug})


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Унвон")
    slug = models.SlugField(unique=True, blank=True)
    poet = models.ForeignKey(Poet, on_delete=models.CASCADE, related_name='books', verbose_name="Шоир")
    description = models.TextField(blank=True, verbose_name="Тавзеҳ")
    publication_date = models.DateField(null=True, blank=True, verbose_name="Санаи нашр")
    cover_image = models.ImageField(upload_to='books/', null=True, blank=True, verbose_name="Акси рӯи китоб")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Китоб"
        verbose_name_plural = "Китобҳо"
        ordering = ['-publication_date']

    def __str__(self):
        return f"{self.title} - {self.poet.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})


class Poem(models.Model):
    title = models.CharField(max_length=200, verbose_name="Унвон")
    slug = models.SlugField(blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='poems', verbose_name="Китоб")
    content = models.TextField(verbose_name="Матн")
    order = models.PositiveIntegerField(default=0, verbose_name="Тартиб")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Шеър"
        verbose_name_plural = "Шеърҳо"
        ordering = ['order', 'title']
        unique_together = ['book', 'slug']

    def __str__(self):
        return f"{self.title} - {self.book.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('poem_detail', kwargs={'book_slug': self.book.slug, 'poem_slug': self.slug})

    def get_previous_poem(self):
        return self.book.poems.filter(order__lt=self.order).last()

    def get_next_poem(self):
        return self.book.poems.filter(order__gt=self.order).first()
