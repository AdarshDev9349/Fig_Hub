# Generated by Django 5.0.3 on 2024-04-05 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fig', '0009_remove_profile_figma_file_delete_files_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.CharField(default='User', max_length=10),
        ),
    ]
