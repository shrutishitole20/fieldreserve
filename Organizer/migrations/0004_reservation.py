# Generated by Django 5.1.6 on 2025-03-20 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organizer', '0003_rename_host_tournament_host_match_and_more'),
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
                ('time_slot', models.CharField(choices=[('5:00 - 6:00', '5:00 - 6:00'), ('6:00 - 7:00', '6:00 - 7:00'), ('7:00 - 8:00', '7:00 - 8:00')], max_length=20)),
                ('transaction_id', models.CharField(blank=True, max_length=50)),
                ('payment_status', models.CharField(default='Pending', max_length=20)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
