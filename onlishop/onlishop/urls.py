from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('store.urls'))
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
