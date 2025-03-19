from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('cafes.urls', namespace='cafes')),
    path('api/users/', include('users.urls')),
    path('users/', include('users.urls')),
    path('reviews/',include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
