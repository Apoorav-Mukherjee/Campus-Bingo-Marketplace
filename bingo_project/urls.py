from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('', include('marketplace.urls', namespace='marketplace')),
]

# Custom error handlers
handler404 = 'bingo_project.views.error_404'
handler403 = 'bingo_project.views.error_403'
handler500 = 'bingo_project.views.error_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)