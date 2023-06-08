# Generated by Django 4.2.1 on 2023-06-08 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_post_image_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_public', models.BooleanField(default=True, help_text='Uncheck this if you do not want this comment to appear on the site.')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.post')),
            ],
            options={
                'ordering': ['-created'],
                'indexes': [models.Index(fields=['created'], name='news_commen_created_cac50c_idx')],
            },
        ),
    ]
