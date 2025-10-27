from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Auth Service funcionando correctamente con Django")

urlpatterns = [
    path('', home),  # Ruta principal
    path('admin/', admin.site.urls),  # Panel de administración
    path('api/', include('users.urls')),  # 👈 Incluye las rutas de la app 'users'
]
