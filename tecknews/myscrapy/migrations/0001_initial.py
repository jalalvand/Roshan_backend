# Generated by Django 5.0.7 on 2024-07-24 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('tag', models.CharField(max_length=200)),
                ('resource', models.TextField()),
            ],
        ),
    ]
