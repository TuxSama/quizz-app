# Generated by Django 5.1.5 on 2025-01-27 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0006_rename_question_question1'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('score', models.FloatField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
