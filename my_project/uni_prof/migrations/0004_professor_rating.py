# Generated by Django 5.1.4 on 2025-01-28 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uni_prof', '0003_remove_professor_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=1, max_digits=2),
            preserve_default=False,
        ),
    ]
