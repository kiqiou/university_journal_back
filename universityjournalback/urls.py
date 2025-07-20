from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/', include('authentication.urls.auth.auth_urls')),
    path('session/', include('journal.urls.session.session_urls')),
    path('discipline/', include('journal.urls.discipline.discipline_urls')),
    path('group/', include('authentication.urls.group.group_urls')),
    path('user/', include('authentication.urls.user.user_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
