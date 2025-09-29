from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from poetry.models import Poet, Book, Poem
import random
from django.utils.text import slugify
from datetime import date


class Command(BaseCommand):
    help = 'Load sample data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading samples'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Poem.objects.all().delete()
            Book.objects.all().delete()
            Poet.objects.all().delete()

        self.create_sample_poets()
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data')
        )

    def create_sample_poets(self):
        sample_poets = [
            {
                'name': 'Рӯдакӣ',
                'birth_date': date(858, 1, 1),
                'death_date': date(941, 1, 1),
                'biography': 'Абӯ Абдуллоҳи Ҷаъфари ибни Муҳаммад Рӯдакӣ - шоири машҳури тоҷик ва пири шеъри форсӣ-тоҷикӣ.',
                'birth_place': 'Рӯдак',
                'nationality': 'Тоҷик',
                'is_featured': True,
            },
            {
                'name': 'Фирдавсӣ',
                'birth_date': date(940, 1, 1),
                'death_date': date(1020, 1, 1),
                'biography': 'Абулқосими Фирдавсӣ - шоири бузурги тоҷик, муаллифи "Шоҳнома".',
                'birth_place': 'Тӯс',
                'nationality': 'Тоҷик',
                'is_featured': True,
            },
            {
                'name': 'Ҳофизи Шерозӣ',
                'birth_date': date(1315, 1, 1),
                'death_date': date(1390, 1, 1),
                'biography': 'Хоҷа Шамсуддин Муҳаммад Ҳофизи Шерозӣ - шоири машҳури тоҷик.',
                'birth_place': 'Шероз',
                'nationality': 'Тоҷик',
                'is_featured': True,
            }
        ]

        for poet_data in sample_poets:
            poet, created = Poet.objects.get_or_create(
                name=poet_data['name'],
                defaults=poet_data
            )
            
            if created:
                self.stdout.write(f'Created poet: {poet.name}')
                self.create_sample_books(poet)

    def create_sample_books(self, poet):
        sample_books = [
            {
                'title': f'Девони {poet.name}',
                'description': f'Маҷмӯаи шеърҳои {poet.name}',
                'language': 'Тоҷикӣ',
            },
            {
                'title': f'Интихоби {poet.name}',
                'description': f'Шеърҳои интихобии {poet.name}',
                'language': 'Тоҷикӣ',
            }
        ]

        for book_data in sample_books:
            book_data['poet'] = poet
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                poet=poet,
                defaults=book_data
            )
            
            if created:
                self.stdout.write(f'Created book: {book.title}')
                self.create_sample_poems(book)

    def create_sample_poems(self, book):
        # Create unique poem titles for each book
        poet_name = book.poet.name.split()[-1]  # Get last part of poet name
        sample_poems = [
            {
                'title': f'Баҳори умед - {poet_name}',
                'content': '''Баҳор омад ва дил шод шуд,
Ҷаҳон аз гул обод шуд.
Чаман хандон ва сабз гашт,
Ҳаво хуш ва навожонон.''',
                'order': 1,
            },
            {
                'title': f'Ситораҳои шаб - {poet_name}',
                'content': '''Дар осмони шаби тор,
Ситораҳо чу ҷавҳор.
Нур пошон ба замин,
Шеъри табиат бефинор.''',
                'order': 2,
            },
            {
                'title': f'Дарёи зиндагӣ - {poet_name}',
                'content': '''Зиндагӣ дарё аст,
Ҷорӣ аст, раво аст.
Бо умеду шодӣ,
Ба пеш равон аст.''',
                'order': 3,
            }
        ]

        for poem_data in sample_poems:
            poem_data['book'] = book
            poem, created = Poem.objects.get_or_create(
                title=poem_data['title'],
                book=book,
                defaults=poem_data
            )
            
            if created:
                self.stdout.write(f'Created poem: {poem.title}')