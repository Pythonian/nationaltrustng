from django.core.management.base import BaseCommand
from django.utils.text import slugify

from faker import Faker
from faker.providers import DynamicProvider

from news.models import Category

elements = [
    'Politics',
    'News',
    'Features',
    'Opinion',
    'Personality',
    'Sport',
    'Interview',
    'Economy',
    'Security',
    'Africa',
    'World'
]

category_provider = DynamicProvider(
    provider_name="category",
    elements=elements
)

fake = Faker()
fake.add_provider(category_provider)


class Command(BaseCommand):
    help = 'Populates the database with Categories'

    def handle(self, *args, **kwargs):
        for _ in range(len(elements)):
            Category.objects.get_or_create(
                title=fake.category(),
                slug=slugify(fake.category()))
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(elements)} Categories.'))
