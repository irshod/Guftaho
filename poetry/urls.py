from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

# API Router
router = DefaultRouter()
router.register(r'poets', api_views.PoetViewSet)
router.register(r'books', api_views.BookViewSet)
router.register(r'poems', api_views.PoemViewSet)

app_name = 'poetry'

urlpatterns = [
    # Main pages
    path('', views.home_view, name='home'),
    path('poet/<slug:slug>/', views.poet_detail_view, name='poet_detail'),
    path('book/<slug:slug>/', views.book_detail_view, name='book_detail'),
    path('poem/<slug:slug>/', views.poem_detail_view, name='poem_detail'),
    path('book/<slug:book_slug>/poem/<slug:poem_slug>/', views.poem_detail_view, name='poem_detail_full'),
    
    # Search and filtering
    path('search/', views.search_view, name='search'),
    path('advanced-search/', views.search_view, name='advanced_search'),
    
    # User features (require authentication)
    path('favorites/', views.favorites_view, name='favorites'),
    path('reading-history/', views.reading_history_view, name='reading_history'),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    
    # Statistics and analytics
    path('statistics/', views.statistics_view, name='statistics'),
    
    # API endpoints
    path('api/', include(router.urls)),
]