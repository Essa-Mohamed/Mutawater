# Generated by Django 5.2.4 on 2025-07-18 02:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='نص الشكوى')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='المستخدم')),
            ],
            options={
                'verbose_name': 'شكوى',
                'verbose_name_plural': 'الشكاوى',
                'ordering': ['-created'],
            },
        ),
    ]
