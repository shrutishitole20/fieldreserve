# Generated by Django 5.1.6 on 2025-03-20 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0004_rating_created_at_alter_rating_ground_name_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='rating',
            name='Ground_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='rating',
            name='ground_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='rating',
            name='star',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rating',
            name='uid',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.RemoveField(
            model_name='rating',
            name='created_at',
        ),
    ]
