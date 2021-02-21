# Generated by Django 3.1.3 on 2021-01-19 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('user_type', models.IntegerField()),
                ('date_registered', models.DateField()),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('active', models.BooleanField()),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('gender', models.IntegerField()),
                ('DOB', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Certificates',
            fields=[
                ('doctor_id', models.ForeignKey(db_column='doctor_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='signup.users')),
                ('certificate', models.FileField(upload_to='')),
                ('specialization_area', models.CharField(max_length=50)),
            ],
        ),
    ]