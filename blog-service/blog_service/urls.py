# blog_service/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connections
from django.core.cache import cache

def healthz(request):
    """Verifica conexión con PostgreSQL y Redis"""
    db_ok = False
    redis_ok = False
    try:
        connections['default'].cursor()
        db_ok = True
    except Exception:
        db_ok = False
    try:
        cache.set("healthcheck", "ok", 5)
        redis_ok = cache.get("healthcheck") == "ok"
    except Exception:
        redis_ok = False

    status = 200 if (db_ok and redis_ok) else 503
    return JsonResponse({"db": db_ok, "redis": redis_ok}, status=status)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz", healthz),
    path("api/categories/", include("categories.urls")),
    path("api/posts/", include("posts.urls")),
]
