import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guftaho.settings')
django.setup()

from poetry.models import Poet, Book, Poem
from django.utils.text import slugify
import unicodedata
import re

def custom_slugify(value):
    """Custom slugify function that handles non-Latin characters better"""
    # Remove diacritics and convert to ASCII if possible
    value = str(value)
    
    # For Persian/Tajik characters, create a simple transliteration
    persian_map = {
        'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's', 'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh',
        'د': 'd', 'ذ': 'z', 'ر': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'd',
        'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'q', 'ک': 'k', 'گ': 'g', 'ل': 'l',
        'م': 'm', 'ن': 'n', 'و': 'v', 'ه': 'h', 'ی': 'y', 'ء': '', 'آ': 'a', 'أ': 'a', 'إ': 'e',
        'ة': 'h', 'ى': 'a', 'ئ': 'y', 'ؤ': 'v',
        # Tajik specific
        'ӣ': 'i', 'ӯ': 'u', 'ҳ': 'h', 'қ': 'q', 'ғ': 'gh', 'ҷ': 'j', 'ҳ': 'h'
    }
    
    # Replace Persian/Tajik characters
    for persian, latin in persian_map.items():
        value = value.replace(persian, latin)
    
    # Use Django's slugify
    slug = slugify(value)
    
    # If still empty, create a fallback
    if not slug:
        # Create a simple slug from the original name
        slug = re.sub(r'[^\w\s-]', '', value).strip().lower()
        slug = re.sub(r'[-\s]+', '-', slug)
        if not slug:
            slug = 'poet'  # fallback
    
    return slug

def fix_slugs():
    """Fix empty slugs for all models"""
    print("Fixing poet slugs...")
    
    poets = Poet.objects.all()
    for poet in poets:
        if not poet.slug:
            new_slug = custom_slugify(poet.name)
            print(f'Updating poet "{poet.name}" with slug: "{new_slug}"')
            poet.slug = new_slug
            poet.save()
    
    print("Fixing book slugs...")
    books = Book.objects.all()
    for book in books:
        if not book.slug:
            new_slug = custom_slugify(book.title)
            print(f'Updating book "{book.title}" with slug: "{new_slug}"')
            book.slug = new_slug
            book.save()
    
    print("Fixing poem slugs...")
    poems = Poem.objects.all()
    for poem in poems:
        if not poem.slug:
            new_slug = custom_slugify(poem.title)
            print(f'Updating poem "{poem.title}" with slug: "{new_slug}"')
            poem.slug = new_slug
            poem.save()
    
    print("Checking for duplicates and fixing...")
    # Check for duplicate slugs and fix them
    for model_class in [Poet, Book, Poem]:
        slugs = {}
        for obj in model_class.objects.all():
            if obj.slug in slugs:
                # Duplicate found, append number
                counter = 1
                new_slug = f"{obj.slug}-{counter}"
                while model_class.objects.filter(slug=new_slug).exists():
                    counter += 1
                    new_slug = f"{obj.slug}-{counter}"
                print(f'Fixing duplicate slug for {model_class.__name__} "{obj}": "{obj.slug}" -> "{new_slug}"')
                obj.slug = new_slug
                obj.save()
            slugs[obj.slug] = obj
    
    print("Done!")

if __name__ == '__main__':
    fix_slugs()