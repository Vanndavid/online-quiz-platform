# Generated by Django 5.0.4 on 2024-05-12 08:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0004_alter_choice_question'),
        ('quiz', '0002_quiz_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestion',
            name='choice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='question.choice'),
        ),
    ]
