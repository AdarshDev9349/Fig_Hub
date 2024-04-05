# Generated by Django 5.0.3 on 2024-04-05 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fig', '0008_files_remove_profile_figma_file_profile_figma_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='figma_file',
        ),
        migrations.DeleteModel(
            name='files',
        ),
        migrations.AddField(
            model_name='profile',
            name='figma_file',
            field=models.URLField(default=5),
            preserve_default=False,
        ),
    ]
