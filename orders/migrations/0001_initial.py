# Generated by Django 2.0.3 on 2020-05-08 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu_Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('small', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('large', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
            ],
        ),
    ]
