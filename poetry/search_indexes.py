from haystack import indexes
from .models import Poet, Book, Poem


class PoetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    biography = indexes.CharField(model_attr='biography')
    birth_date = indexes.DateField(model_attr='birth_date', null=True)
    death_date = indexes.DateField(model_attr='death_date', null=True)

    def get_model(self):
        return Poet

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    poet = indexes.CharField(model_attr='poet__name')
    publication_date = indexes.DateField(model_attr='publication_date', null=True)

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        return self.get_model().objects.select_related('poet')


class PoemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    book_title = indexes.CharField(model_attr='book__title')
    poet_name = indexes.CharField(model_attr='book__poet__name')
    order = indexes.IntegerField(model_attr='order')

    def get_model(self):
        return Poem

    def index_queryset(self, using=None):
        return self.get_model().objects.select_related('book__poet')