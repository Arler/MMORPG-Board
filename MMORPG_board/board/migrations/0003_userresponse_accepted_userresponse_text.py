# Generated by Django 5.0.4 on 2024-05-06 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresponse',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userresponse',
            name='text',
            field=models.TextField(default='1'),
            preserve_default=False,
        ),
    ]
