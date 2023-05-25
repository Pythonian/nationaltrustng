from django.core.management.base import BaseCommand
from django.utils.text import slugify

from news.models import Category

categories = [
    'Politics',
    'News',
    'Features',
    'Opinion',
    'Personality',
    'Sports',
    'Interview',
    'Economy',
    'Entertainment',
    'Security',
    'Africa',
    'World',
    'Editorial'
]

class Command(BaseCommand):
    help = 'Populates the database with Categories'
    
    def handle(self, *args, **kwargs):
        order = 1
        for category_title in categories:
            slug = slugify(category_title)

            # Check if category with same slug already exists
            if Category.objects.filter(slug=slug).exists():
                continue

            category = Category(
                title=category_title,
                slug=slug,
                order=order
            )
            category.save()

            order += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(categories)} Categories.'))
