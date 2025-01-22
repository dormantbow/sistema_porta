
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doors/', include('doors.urls')),  # Certifique-se de que isso está presente
]