# Generated by Django 5.0.4 on 2024-05-11 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_remove_announcement_file_remove_userresponse_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponsemedia',
            name='obj',
        ),
        migrations.DeleteModel(
            name='AnnouncementMedia',
        ),
        migrations.DeleteModel(
            name='UserResponseMedia',
        ),
    ]
