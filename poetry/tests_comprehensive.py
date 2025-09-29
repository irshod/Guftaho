from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from poetry.models import Poet, Book, Poem, Favorite, ReadingHistory
from datetime import date
import json


class PoetModelTest(TestCase):
    def setUp(self):
        self.poet = Poet.objects.create(
            name='Test Poet',
            biography='A test poet for testing purposes',
            birth_date=date(1900, 1, 1),
            death_date=date(1980, 1, 1)
        )

    def test_poet_creation(self):
        self.assertEqual(self.poet.name, 'Test Poet')
        self.assertTrue(self.poet.slug)  # Should auto-generate slug
        self.assertEqual(self.poet.age_at_death, 80)
        self.assertFalse(self.poet.is_alive)

    def test_poet_absolute_url(self):
        url = self.poet.get_absolute_url()
        self.assertEqual(url, f'/poet/{self.poet.slug}/')

    def test_increment_view_count(self):
        initial_count = self.poet.view_count
        self.poet.increment_view_count()
        self.poet.refresh_from_db()
        self.assertEqual(self.poet.view_count, initial_count + 1)


class BookModelTest(TestCase):
    def setUp(self):
        self.poet = Poet.objects.create(
            name='Test Poet',
            biography='A test poet'
        )
        self.book = Book.objects.create(
            title='Test Book',
            poet=self.poet,
            description='A test book',
            publication_date=date(2020, 1, 1)
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.poet, self.poet)
        self.assertTrue(self.book.slug)

    def test_book_str_representation(self):
        expected = f"{self.book.title} - {self.poet.name}"
        self.assertEqual(str(self.book), expected)


class PoemModelTest(TestCase):
    def setUp(self):
        self.poet = Poet.objects.create(name='Test Poet', biography='Test')
        self.book = Book.objects.create(title='Test Book', poet=self.poet)
        self.poem = Poem.objects.create(
            title='Test Poem',
            book=self.book,
            content='This is a test poem\nWith multiple lines\nFor testing purposes',
            order=1
        )

    def test_poem_creation(self):
        self.assertEqual(self.poem.title, 'Test Poem')
        self.assertEqual(self.poem.book, self.book)
        self.assertTrue(self.poem.slug)

    def test_word_and_line_count_calculation(self):
        # Should auto-calculate on save
        self.assertEqual(self.poem.word_count, 9)  # 9 words in the content
        self.assertEqual(self.poem.line_count, 3)  # 3 lines

    def test_reading_time_calculation(self):
        # Should be at least 1 minute
        self.assertGreaterEqual(self.poem.reading_time, 1)

    def test_navigation_methods(self):
        # Create another poem in the same book
        poem2 = Poem.objects.create(
            title='Second Poem',
            book=self.book,
            content='Another test poem',
            order=2
        )
        
        # Test navigation
        self.assertEqual(self.poem.get_next_poem(), poem2)
        self.assertEqual(poem2.get_previous_poem(), self.poem)
        self.assertIsNone(self.poem.get_previous_poem())
        self.assertIsNone(poem2.get_next_poem())


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.poet = Poet.objects.create(name='Test Poet', biography='Test')
        self.book = Book.objects.create(title='Test Book', poet=self.poet)
        self.poem = Poem.objects.create(
            title='Test Poem',
            book=self.book,
            content='Test content',
            order=1
        )

    def test_home_view(self):
        response = self.client.get(reverse('poetry:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poet.name)

    def test_poet_detail_view(self):
        response = self.client.get(
            reverse('poetry:poet_detail', kwargs={'slug': self.poet.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poet.name)

    def test_book_detail_view(self):
        response = self.client.get(
            reverse('poetry:book_detail', kwargs={'slug': self.book.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_poem_detail_view(self):
        response = self.client.get(
            reverse('poetry:poem_detail', kwargs={
                'book_slug': self.book.slug,
                'poem_slug': self.poem.slug
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poem.title)

    def test_search_view(self):
        response = self.client.get(
            reverse('poetry:search'),
            {'q': 'Test'}
        )
        self.assertEqual(response.status_code, 200)

    def test_view_count_increment(self):
        initial_count = self.poet.view_count
        self.client.get(
            reverse('poetry:poet_detail', kwargs={'slug': self.poet.slug})
        )
        self.poet.refresh_from_db()
        self.assertEqual(self.poet.view_count, initial_count + 1)


class UserFeaturesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.poet = Poet.objects.create(name='Test Poet', biography='Test')
        self.book = Book.objects.create(title='Test Book', poet=self.poet)
        self.poem = Poem.objects.create(
            title='Test Poem',
            book=self.book,
            content='Test content',
            order=1
        )

    def test_toggle_favorite_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Add to favorites
        response = self.client.post(
            reverse('poetry:toggle_favorite'),
            {
                'content_type': 'poem',
                'object_id': self.poem.id
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['is_favorited'])
        
        # Check favorite was created
        self.assertTrue(
            Favorite.objects.filter(
                user=self.user,
                content_type='poem',
                object_id=self.poem.id
            ).exists()
        )
        
        # Remove from favorites
        response = self.client.post(
            reverse('poetry:toggle_favorite'),
            {
                'content_type': 'poem',
                'object_id': self.poem.id
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['is_favorited'])

    def test_toggle_favorite_unauthenticated(self):
        response = self.client.post(
            reverse('poetry:toggle_favorite'),
            {
                'content_type': 'poem',
                'object_id': self.poem.id
            }
        )
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_reading_history_creation(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Visit poem detail page
        response = self.client.get(
            reverse('poetry:poem_detail', kwargs={
                'book_slug': self.book.slug,
                'poem_slug': self.poem.slug
            })
        )
        self.assertEqual(response.status_code, 200)
        
        # Check reading history was created
        self.assertTrue(
            ReadingHistory.objects.filter(
                user=self.user,
                poem=self.poem
            ).exists()
        )

    def test_favorites_view(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Create a favorite
        Favorite.objects.create(
            user=self.user,
            content_type='poem',
            object_id=self.poem.id
        )
        
        response = self.client.get(reverse('poetry:favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poem.title)

    def test_reading_history_view(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Create reading history
        ReadingHistory.objects.create(
            user=self.user,
            poem=self.poem
        )
        
        response = self.client.get(reverse('poetry:reading_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poem.title)


class SearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.poet = Poet.objects.create(
            name='Ҳофизи Шерозӣ',
            biography='Шоири машҳури тоҷик'
        )
        self.book = Book.objects.create(
            title='Девони Ҳофиз',
            poet=self.poet,
            description='Маҷмӯаи ғазалҳои Ҳофиз'
        )
        self.poem = Poem.objects.create(
            title='Ғазали зебо',
            book=self.book,
            content='Дил ба дасти тӯ сипурдам',
            order=1
        )

    def test_search_poems(self):
        response = self.client.get(
            reverse('poetry:search'),
            {'q': 'ғазал', 'content_type': 'poems'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poem.title)

    def test_search_books(self):
        response = self.client.get(
            reverse('poetry:search'),
            {'q': 'девон', 'content_type': 'books'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_search_poets(self):
        response = self.client.get(
            reverse('poetry:search'),
            {'q': 'ҳофиз', 'content_type': 'poets'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.poet.name)

    def test_search_all_content(self):
        response = self.client.get(
            reverse('poetry:search'),
            {'q': 'ҳофиз', 'content_type': 'all'}
        )
        self.assertEqual(response.status_code, 200)
        # Should find content related to Ҳофиз