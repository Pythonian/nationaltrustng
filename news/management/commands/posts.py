import random
import requests
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from faker import Faker
from PIL import Image
from io import BytesIO
from news.models import Category, Post


#                     img_temp = NamedTemporaryFile(delete=True)
#                     img_temp.write(image_response.content)
#                     img_temp.flush()


fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with sample data for the Post model'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of posts to be created')

    def handle(self, *args, **kwargs):
        categories = Category.objects.all()
        total = kwargs['total']
        paragraphs = fake.paragraphs(nb=50)
        text = '\n\n'.join(paragraphs)

        # Download images from the API
        api_url = "https://picsum.photos/v2/list?page=1&limit=100"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            images = [item['download_url'] for item in data]
        else:
            images = []

        for _ in range(total):
            title = fake.sentence()
            slug = slugify(title)
            author = User.objects.get(id=1)
            category = random.choice(categories)
            body = text
            page_views = fake.random_int(min=1, max=1000)
            read_time = fake.random_int(min=1, max=10)
            created = fake.date_this_year()

            # Download and crop image for the post
            if images:
                image_url = random.choice(images)
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    # Open the image using Pillow
                    image = Image.open(BytesIO(image_response.content))

                    # Resize and crop the image
                    image = image.resize((960, 520))
                    width, height = image.size
                    left = (width - 960) / 2
                    top = (height - 520) / 2
                    right = (width + 960) / 2
                    bottom = (height + 520) / 2
                    image = image.crop((left, top, right, bottom))

                    # Create a temporary file to save the image
                    img_temp = NamedTemporaryFile(delete=True)
                    image.save(img_temp, format='JPEG')
                    img_temp.flush()

                    # Set the image field of the Post model
                    image_filename = image_url.split('/')[-1]
                    image_filename = f"{image_filename}.jpg"
                    image = File(img_temp, name=image_filename)
                else:
                    image = 'post.jpg'  # Set default image filename
            else:
                image = 'post.jpg'  # Set default image filename

            Post.objects.create(
                title=title,
                slug=slug,
                author=author,
                category=category,
                body=body,
                page_views=page_views,
                image=image,
                read_time=read_time,
                created=created
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully added {total} Posts.'))
