# Generated by Django 4.2.2 on 2023-06-07 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0003_alter_rssidataless_id_alter_rssidatamore_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rssidataless',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='rssidatamore',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]