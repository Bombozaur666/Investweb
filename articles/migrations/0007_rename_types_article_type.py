# Generated by Django 4.1 on 2022-08-12 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_article_types'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='types',
            new_name='type',
        ),
    ]
