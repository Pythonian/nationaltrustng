# Generated by Django 4.2.1 on 2023-06-26 13:55

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='body'),
        ),
    ]
