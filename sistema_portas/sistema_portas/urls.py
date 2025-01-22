from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('portas.urls')),
    #path('api/portas/', include('portas.urls'), name="portas"),
]
