import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guftaho.settings')
django.setup()

from poetry.models import Poet, Book, Poem

# Check for empty slugs
poets = Poet.objects.all()
print(f'Total poets: {poets.count()}')

empty_slug_poets = [p for p in poets if not p.slug]
print(f'Poets with empty slugs: {len(empty_slug_poets)}')
for p in empty_slug_poets[:5]:
    print(f'- "{p.name}": slug="{p.slug}"')

# Check for None slugs
none_slug_poets = [p for p in poets if p.slug is None]
print(f'Poets with None slugs: {len(none_slug_poets)}')

# Show some sample poet data
print('\nSample poets:')
for p in poets[:5]:
    print(f'- "{p.name}": slug="{p.slug}"')

# Check books
books = Book.objects.all()
print(f'\nTotal books: {books.count()}')
empty_slug_books = [b for b in books if not b.slug]
print(f'Books with empty slugs: {len(empty_slug_books)}')
for b in empty_slug_books[:3]:
    print(f'- "{b.title}": slug="{b.slug}"')

# Check poems  
poems = Poem.objects.all()
print(f'\nTotal poems: {poems.count()}')
empty_slug_poems = [p for p in poems if not p.slug]
print(f'Poems with empty slugs: {len(empty_slug_poems)}')
for p in empty_slug_poems[:3]:
    print(f'- "{p.title}": slug="{p.slug}"')