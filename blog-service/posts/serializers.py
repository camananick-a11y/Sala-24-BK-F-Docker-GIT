from rest_framework import serializers
from .models import Post
from authors.serializers import AuthorSerializer
from categories.serializers import CategorySerializer
from django.utils.text import Truncator

class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "excerpt", "author", "category", "published_at"]

    def get_excerpt(self, obj):
        return Truncator(obj.body).chars(150)

class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "body", "author", "category", "published_at", "views"]
