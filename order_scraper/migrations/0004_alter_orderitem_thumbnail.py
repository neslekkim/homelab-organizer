# Generated by Django 3.2.18 on 2023-04-12 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_scraper', '0003_auto_20230412_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='thumbnail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order_scraper.attachement'),
        ),
    ]
