import django_filters
from django import forms
from .models import Poet, Book, Poem


class PoetFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ном...'})
    )
    birth_year = django_filters.NumberFilter(
        field_name='birth_date__year',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Соли таваллуд...'})
    )
    death_year = django_filters.NumberFilter(
        field_name='death_date__year',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Соли вафот...'})
    )

    class Meta:
        model = Poet
        fields = ['name', 'birth_year', 'death_year']


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Унвони китоб...'})
    )
    poet = django_filters.ModelChoiceFilter(
        queryset=Poet.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    publication_year = django_filters.NumberFilter(
        field_name='publication_date__year',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Соли нашр...'})
    )

    class Meta:
        model = Book
        fields = ['title', 'poet', 'publication_year']


class PoemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Унвони шеър...'})
    )
    content = django_filters.CharFilter(
        field_name='content',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Матни шеър...'})
    )
    book = django_filters.ModelChoiceFilter(
        queryset=Book.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    poet = django_filters.ModelChoiceFilter(
        field_name='book__poet',
        queryset=Poet.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Poem
        fields = ['title', 'content', 'book', 'poet']


class AdvancedSearchFilter(django_filters.FilterSet):
    """Advanced search filter for cross-model searching"""
    q = django_filters.CharFilter(
        method='search_all',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ҷустуҷӯ дар ҳама маводҳо...'
        })
    )
    content_type = django_filters.ChoiceFilter(
        choices=[
            ('all', 'Ҳама'),
            ('poets', 'Шоирон'),
            ('books', 'Китобҳо'),
            ('poems', 'Шеърҳо'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def search_all(self, queryset, name, value):
        """Search across all models"""
        if not value:
            return queryset
        
        # This will be implemented in the view
        return queryset

    class Meta:
        model = Poem  # Base model
        fields = ['q', 'content_type']