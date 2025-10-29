from django.db import models
from slugify import slugify

class Post(models.Model):
    STATUS_CHOICES = (("published","published"), ("draft","draft"))

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey("authors.Author", on_delete=models.CASCADE)
    category = models.ForeignKey("categories.Category", on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:300]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
