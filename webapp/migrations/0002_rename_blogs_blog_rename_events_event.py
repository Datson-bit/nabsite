# Generated by Django 4.2.7 on 2024-09-24 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blogs',
            new_name='Blog',
        ),
        migrations.RenameModel(
            old_name='Events',
            new_name='Event',
        ),
    ]