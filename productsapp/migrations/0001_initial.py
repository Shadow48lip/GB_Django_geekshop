# Generated by Django 3.2.9 on 2021-12-16 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='имя')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='создано')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='обновлено')),
            ],
        ),
    ]