# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('name', models.CharField(max_length=20, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThroughStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arriveTime', models.DateTimeField()),
                ('departureTime', models.DateTimeField()),
                ('staName', models.ForeignKey(to='ticket.Station')),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('trainNo', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('seatNum', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='throughstation',
            name='trainNo',
            field=models.ForeignKey(to='ticket.Train'),
        ),
    ]
