# Generated by Django 3.2 on 2021-04-16 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210416_1258'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date'], 'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
    ]
