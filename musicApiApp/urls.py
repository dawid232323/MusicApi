from django.urls import path
from musicApiApp.views import AlbumView
from musicApiApp.views.genre_view import GenreView

urlpatterns = [
    path('albums', AlbumView.as_view({
        'post': 'create',
        'get': 'list'
    })),
    path('albums/<int:album_id>', AlbumView.as_view({
        'get': 'retrieve'
    })),
    path('genres', GenreView.as_view({
        'post': 'create',
        'get': 'list'
    })),
    path('genres/<int:genre_id>', GenreView.as_view({
        'get': 'retrieve'
    }))
]
