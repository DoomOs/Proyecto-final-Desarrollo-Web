# Generated by Django 4.2.4 on 2023-10-17 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='user',
        ),
        migrations.AddField(
            model_name='card',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='board.project'),
        ),
    ]
