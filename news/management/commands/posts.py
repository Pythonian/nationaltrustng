import random

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth.models import User

from faker import Faker

from news.models import Category, Post

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with sample data for the Post model'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of posts to be created')

    def handle(self, *args, **kwargs):
        categories = Category.objects.all()
        total = kwargs['total']
        paragraphs = fake.paragraphs(nb=10)
        text = '\n\n'.join(paragraphs)

        for _ in range(total):
            title = fake.sentence()
            slug = slugify(title)
            author = User.objects.get(id=1)
            category = random.choice(categories)
            body = text
            page_views = fake.random_int(min=1, max=1000)
            read_time = fake.random_int(min=1, max=10)
            created = fake.date_this_year()

            Post.objects.create(
                title=title,
                slug=slug,
                author=author,
                category=category,
                body=body,
                page_views=page_views,
                read_time=read_time,
                created=created
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully added {total} Posts.'))
