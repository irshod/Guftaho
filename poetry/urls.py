from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('poet/<slug:slug>/', views.poet_detail_view, name='poet_detail'),
    path('book/<slug:slug>/', views.book_detail_view, name='book_detail'),
    path('book/<slug:book_slug>/poem/<slug:poem_slug>/', views.poem_detail_view, name='poem_detail'),
    path('search/', views.search_view, name='search'),
]