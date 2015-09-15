# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20150915_0147'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('totSeat', models.IntegerField()),
                ('seatMap', models.CharField(max_length=200)),
                ('departure', models.ForeignKey(related_name='depStation', to='ticket.ThroughStation')),
                ('destination', models.ForeignKey(related_name='desStation', to='ticket.ThroughStation')),
            ],
        ),
    ]
