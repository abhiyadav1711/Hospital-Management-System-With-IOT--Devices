import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('specialization', models.CharField(max_length=120)),
                ('experience_years', models.PositiveIntegerField(default=0)),
                ('availability', models.CharField(choices=[('Available', 'Available'), ('Busy', 'Busy')], default='Available', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=10)),
                ('disease', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('Admitted', 'Admitted'), ('Discharged', 'Discharged'), ('Critical', 'Critical')], default='Admitted', max_length=20)),
                ('contact', models.CharField(blank=True, max_length=20)),
                ('device_id', models.CharField(blank=True, help_text="ESP32 device ID sending this patient's vitals, e.g. ESP32-01", max_length=50, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.CharField(choices=[('Confirmed', 'Confirmed'), ('Waiting', 'Waiting'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Confirmed', max_length=20)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='hospital.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='hospital.patient')),
            ],
            options={
                'ordering': ['-date', '-time'],
            },
        ),
        migrations.CreateModel(
            name='VitalReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heart_rate', models.PositiveIntegerField(help_text='BPM')),
                ('spo2', models.PositiveIntegerField(help_text='Blood oxygen %')),
                ('temperature', models.FloatField(help_text='Body temp in Fahrenheit')),
                ('bp_systolic', models.PositiveIntegerField(default=120)),
                ('bp_diastolic', models.PositiveIntegerField(default=80)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vitals', to='hospital.patient')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultation_fee', models.PositiveIntegerField(default=500)),
                ('room_charges', models.PositiveIntegerField(default=0)),
                ('medicine_charges', models.PositiveIntegerField(default=0)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='hospital.patient')),
            ],
        ),
    ]