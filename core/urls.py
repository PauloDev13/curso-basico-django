from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('companies/', include('company.urls')),
    path('investors/', include('investors.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
