# Generated by Django 4.1 on 2022-08-20 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_alter_article_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created', 'article')},
        ),
    ]
