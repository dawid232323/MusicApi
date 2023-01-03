from django.urls import path
from musicApiApp.views import AlbumView

urlpatterns = [
    path('albums', AlbumView.as_view({
        'post': 'create',
        'get': 'list'
    })),
    path('albums/<int:album_id>', AlbumView.as_view({
        'get': 'retrieve'
    }))
]
