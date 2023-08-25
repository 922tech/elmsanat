# Generated by Django 4.1.3 on 2023-08-24 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogfile',
            name='title',
            field=models.CharField(max_length=64, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='blogimage',
            name='title',
            field=models.CharField(max_length=64, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=64, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=64, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=64, verbose_name='Title'),
        ),
    ]