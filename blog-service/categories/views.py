
from rest_framework import generics
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Category
from .serializers import CategorySerializer

@method_decorator(cache_page(60), name="dispatch")
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
