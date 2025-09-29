from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag
def safe_url(url_name, *args, **kwargs):
    """
    Safely generate URL, return '#' if any argument is empty or None
    """
    try:
        # Check if any positional arguments are empty
        for arg in args:
            if not arg:
                return '#'
        
        # Check if any keyword arguments are empty
        for key, value in kwargs.items():
            if not value:
                return '#'
        
        return reverse(url_name, args=args, kwargs=kwargs)
    except (NoReverseMatch, AttributeError, TypeError):
        return '#'

@register.simple_tag
def poet_url(poet):
    """
    Safely generate poet detail URL
    """
    if not poet or not hasattr(poet, 'slug') or not poet.slug:
        return '#'
    
    try:
        return reverse('poetry:poet_detail', kwargs={'slug': poet.slug})
    except (NoReverseMatch, AttributeError):
        return '#'

@register.simple_tag  
def book_url(book):
    """
    Safely generate book detail URL
    """
    if not book or not hasattr(book, 'slug') or not book.slug:
        return '#'
    
    try:
        return reverse('poetry:book_detail', kwargs={'slug': book.slug})
    except (NoReverseMatch, AttributeError):
        return '#'

@register.simple_tag
def poem_url(book, poem):
    """
    Safely generate poem detail URL
    """
    if not book or not poem or not hasattr(book, 'slug') or not hasattr(poem, 'slug'):
        return '#'
    
    if not book.slug or not poem.slug:
        return '#'
    
    try:
        return reverse('poetry:poem_detail', kwargs={'book_slug': book.slug, 'slug': poem.slug})
    except (NoReverseMatch, AttributeError):
        return '#'