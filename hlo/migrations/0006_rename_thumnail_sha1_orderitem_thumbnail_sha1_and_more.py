# Generated by Django 4.2.13 on 2024-05-12 18:33

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
        ("hlo", "0005_rename_thumnail_sha1_stockitem_thumbnail_sha1_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderitem",
            old_name="thumnail_sha1",
            new_name="thumbnail_sha1",
        ),
        migrations.AlterField(
            model_name="stockitem",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text=None,
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
