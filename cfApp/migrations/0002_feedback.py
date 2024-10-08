# Generated by Django 4.2.7 on 2024-04-29 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cfApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('feedback', models.CharField(max_length=500)),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cfApp.users')),
            ],
        ),
    ]
