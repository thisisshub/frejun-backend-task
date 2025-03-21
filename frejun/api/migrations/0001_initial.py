# Generated by Django 4.2.19 on 2025-03-10 12:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('distance', models.PositiveIntegerField()),
                ('intermediate_stations', models.JSONField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('station_name', models.CharField(max_length=255)),
                ('station_code', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('age', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=255)),
                ('is_child', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('train_name', models.CharField(max_length=255)),
                ('train_number', models.CharField(max_length=255)),
                ('total_confirmed_berths', models.PositiveIntegerField(default=63)),
                ('total_rac_berths', models.PositiveIntegerField(default=9)),
                ('available_confirmed_berths', models.PositiveIntegerField(default=63)),
                ('available_rac_spots', models.PositiveIntegerField(default=18)),
                ('waiting_list_count', models.PositiveIntegerField(default=0)),
                ('lower_berths_available', models.PositiveIntegerField(default=21)),
                ('middle_berths_available', models.PositiveIntegerField(default=21)),
                ('upper_berths_available', models.PositiveIntegerField(default=21)),
                ('side_lower_berths_available', models.PositiveIntegerField(default=9)),
                ('side_upper_berths_available', models.PositiveIntegerField(default=9)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route', to='api.route')),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='destination_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_station', to='api.station'),
        ),
        migrations.AddField(
            model_name='route',
            name='source_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_station', to='api.station'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booking_status', models.CharField(blank=True, choices=[('RAC', 'RAC'), ('WAITING_LIST', 'WAITING_LIST'), ('CONFIRMED', 'CONFIRMED')], max_length=255, null=True)),
                ('berth_type', models.CharField(blank=True, choices=[('LOWER', 'LOWER'), ('MIDDLE', 'MIDDLE'), ('UPPER', 'UPPER'), ('SIDE_LOWER', 'SIDE_LOWER'), ('NO_BERTH', 'NO_BERTH')], max_length=255, null=True)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='train', to='api.train')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='api.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='train',
            constraint=models.CheckConstraint(check=models.Q(('waiting_list_count__lte', 10)), name='max_waiting_list_10'),
        ),
    ]
