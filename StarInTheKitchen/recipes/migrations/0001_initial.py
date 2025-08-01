# Generated by Django 5.2.4 on 2025-07-08 16:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('ingredients', models.TextField()),
                ('description', models.TextField()),
                ('instructions', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/')),
                ('prep_time', models.PositiveIntegerField(help_text='In minutes')),
                ('cook_time', models.PositiveIntegerField(help_text='In minutes')),
                ('servings', models.PositiveIntegerField()),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cooking_methods', models.ManyToManyField(blank=True, to='categories.cookingmethod')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('diets', models.ManyToManyField(blank=True, to='categories.diet')),
                ('meal_types', models.ManyToManyField(blank=True, to='categories.mealtype')),
                ('occasions', models.ManyToManyField(blank=True, to='categories.occasion')),
                ('seasons', models.ManyToManyField(blank=True, to='categories.season')),
            ],
        ),
    ]
