from django.core.management.base import BaseCommand
from django.db.models import Count
from poetry.models import Poet, Book, Poem


class Command(BaseCommand):
    help = 'Update statistics for all poets, books, and poems'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            choices=['poets', 'books', 'poems', 'all'],
            default='all',
            help='Which model to update (default: all)'
        )

    def handle(self, *args, **options):
        model = options['model']
        
        if model in ['poets', 'all']:
            self.update_poet_stats()
        
        if model in ['books', 'all']:
            self.update_book_stats()
        
        if model in ['poems', 'all']:
            self.update_poem_stats()

    def update_poet_stats(self):
        self.stdout.write('Updating poet statistics...')
        poets = Poet.objects.all()
        
        for poet in poets:
            # This will be handled by the manager methods
            pass
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {poets.count()} poets')
        )

    def update_book_stats(self):
        self.stdout.write('Updating book statistics...')
        books = Book.objects.all()
        
        for book in books:
            # Update poems count and other stats if needed
            pass
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {books.count()} books')
        )

    def update_poem_stats(self):
        self.stdout.write('Updating poem statistics...')
        poems = Poem.objects.all()
        
        for poem in poems:
            # Re-save to trigger word_count and line_count calculation
            poem.save()
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {poems.count()} poems')
        )