# Generated by Django 4.2.1 on 2023-05-25 07:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_remove_post_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='updated',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
