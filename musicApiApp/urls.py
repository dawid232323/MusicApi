from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from musicApiApp.views import AlbumView, SongView, GenreView, ArtistView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

swagger_schema_view = get_schema_view(
   openapi.Info(
      title="Music API",
      default_version='v1',
      description="RestApi for storing music data",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="dawpylak@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', swagger_schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', swagger_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', swagger_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login_refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('albums', AlbumView.as_view({
        'post': 'create',
        'get': 'list'
    })),
    path('albums/<int:album_id>', AlbumView.as_view({
        'get': 'retrieve',
        'patch': 'update',
        'delete': 'destroy'
    })),
    path('genres', GenreView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('genres/<int:genre_id>', GenreView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('songs', SongView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('songs/<int:song_id>', SongView.as_view({
        'get': 'retrieve',
        'patch': 'update',
        'delete': 'destroy'
    })),
    path('artists', ArtistView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('artists/<int:artist_id>', ArtistView.as_view({
        'get': 'retrieve',
        'patch': 'update',
        'delete': 'destroy'
    }))
]
