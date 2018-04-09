# Generated by Django 2.0.3 on 2018-04-09 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180404_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Convention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roman_num', models.CharField(max_length=10)),
                ('tagline', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
    ]