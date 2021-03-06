# Generated by Django 3.1.6 on 2021-05-07 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=40, verbose_name='full name')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('death_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodsAndMovements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='period or movement')),
                ('start', models.DateField()),
                ('end', models.DateField(blank=True, null=True)),
                ('description', models.CharField(max_length=50, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='sex')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='type')),
                ('description', models.CharField(max_length=50, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('creation_date', models.DateField(blank=True, null=True)),
                ('description', models.CharField(max_length=60, verbose_name='description')),
                ('arttype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.type')),
                ('author', models.ManyToManyField(to='main.Artist')),
                ('pm', models.ManyToManyField(to='main.PeriodsAndMovements')),
            ],
        ),
        migrations.AddField(
            model_name='artist',
            name='sex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sex'),
        ),
    ]
