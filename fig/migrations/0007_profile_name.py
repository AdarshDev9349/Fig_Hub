# Generated by Django 5.0.3 on 2024-04-04 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fig', '0006_alter_profile_figma_file_delete_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default=5, max_length=255),
            preserve_default=False,
        ),
    ]
