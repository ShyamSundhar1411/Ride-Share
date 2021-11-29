# Generated by Django 3.2.9 on 2021-11-29 11:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RideHost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('start_point', models.CharField(blank=True, max_length=500, null=True)),
                ('destination', models.CharField(blank=True, max_length=500, null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('OPEN', 'OPEN'), ('EXPIRED', 'EXPIRED')], default='EXPIRED', max_length=500)),
                ('seats', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('available', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('slug', models.SlugField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RidePool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('CANCELLED', 'CANCELLED')], default='CANCELLED', max_length=500)),
                ('isriding', models.BooleanField(blank=True, default=False, null=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ride.ridehost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='avatar/')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('address', models.TextField(blank=True, max_length=500, null=True)),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
