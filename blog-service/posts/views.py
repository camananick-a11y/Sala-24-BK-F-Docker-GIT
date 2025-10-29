from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer
from django.db.models import Q, F

@method_decorator(cache_page(60), name="retrieve")
class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.filter(status="published").select_related("author", "category")
    lookup_field = "slug"

    def get_serializer_class(self):
        return PostDetailSerializer if self.action == "retrieve" else PostListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(body__icontains=search))
        return qs

    def retrieve(self, request, *args, **kwargs):
        lookup = kwargs.get(self.lookup_field)
        if lookup and lookup.isdigit():
            try:
                obj = Post.objects.get(pk=int(lookup), status="published")
            except Post.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(obj)
            Post.objects.filter(pk=obj.pk).update(views=F('views') + 1)
            return Response(serializer.data)
        response = super().retrieve(request, *args, **kwargs)
        try:
            obj = self.get_object()
            Post.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        except Exception:
            pass
        return response
