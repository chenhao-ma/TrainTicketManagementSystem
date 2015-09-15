from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserProfile(models.Model):
    #links userprofile to a user model instance
    user = models.OneToOneField(User)

    #additional attributes
    idNo = models.CharField(max_length = 20)

    #override the __unicode__() method
    def __unicode__(self):
        return self.user.username

class Station(models.Model):
    name = models.CharField(max_length = 20, primary_key = True)
    def __unicode__(self):
        return self.name

class Train(models.Model):
    trainNo = models.CharField(max_length = 20, primary_key = True)
    seatNum = models.IntegerField()
    trainType = (
        ('G', 'High Speed Railway'),
        ('D', 'Electric Multiple Units'),
        ('K', 'Fast Train'),
        ('Z', 'Direct trains'),
        )
    def __unicode__(self):
        return self.trainNo

class ThroughStation(models.Model):
    trainNo = models.ForeignKey(Train, related_name = 'trainNum')
    staName = models.ForeignKey(Station, related_name = 'stationName')
    arriveTime = models.DateTimeField()
    departureTime = models.DateTimeField()
    def __unicode__(self):
        return "" + str(self.staName) + " on " + str(self.trainNo)

class DirectRoute(models.Model):
    departure = models.ForeignKey(ThroughStation, related_name = 'depStation')
    destination = models.ForeignKey(ThroughStation, related_name = 'desStation')
    totSeat = models.IntegerField()
    seatMap = models.CharField(max_length = 200)

    def __unicode__(self):
        return "" + str(self.departure) + " ---> " + str(self.destination)


import signals





