# Generated by Django 5.0.4 on 2024-05-11 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_alter_userresponse_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresponse',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
