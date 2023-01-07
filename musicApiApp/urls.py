from django.urls import path
from musicApiApp.views import AlbumView
from musicApiApp.views.genre_view import GenreView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login_refresh', TokenRefreshView.as_view(), name='token_refresh'),
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
