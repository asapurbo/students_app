from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from students_project.views import index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('students/', include('studentsapp.urls')),
    path('', include('account.urls'))
]


if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
