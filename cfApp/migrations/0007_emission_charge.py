# Generated by Django 4.2.7 on 2024-05-07 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfApp', '0006_rename_proof_tips_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='emission',
            name='charge',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
