
from django.core.management.base import BaseCommand
from categories.models import Category
from authors.models import Author
from posts.models import Post
from django.utils import timezone
import random

class Command(BaseCommand):
    help = "Seed blog data: categories, authors, posts"

    def handle(self, *args, **options):
        cat_names = ["Tech", "DevOps", "Django", "JavaScript", "News"]
        cats = []
        for name in cat_names:
            c, _ = Category.objects.get_or_create(name=name)
            cats.append(c)

        authors = []
        for i in range(1, 4):
            a, _ = Author.objects.get_or_create(display_name=f"Author {i}", email=f"author{i}@example.com")
            authors.append(a)

        Post.objects.all().delete()
        for i in range(1, 31):
            author = random.choice(authors)
            category = random.choice(cats)
            status = "published" if i % 4 != 0 else "draft"
            pub_at = timezone.now() if status == "published" else None
            Post.objects.create(
                title=f"Sample Post {i}",
                body=("Lorem ipsum " * 30) + f" (post {i})",
                author=author,
                category=category,
                status=status,
                published_at=pub_at
            )
        self.stdout.write(self.style.SUCCESS("Seed completed"))
