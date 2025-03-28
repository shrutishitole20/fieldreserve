# Generated by Django 5.1.6 on 2025-03-20 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organizer', '0005_delete_reservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateField()),
                ('time_slot', models.CharField(max_length=20)),
            ],
        ),
    ]
