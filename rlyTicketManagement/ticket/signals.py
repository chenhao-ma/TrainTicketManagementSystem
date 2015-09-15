from django.db.models.signals import post_save
from ticket.models import ThroughStation, DirectRoute, Train
from django.dispatch import receiver

@receiver(post_save, sender = ThroughStation)
def directRouteHandler(sender, instance, signal, created, **kwargs):
    if created:
        throughList = ThroughStation.objects.filter(trainNo = instance.trainNo)
        for item in throughList:
            temp = instance.trainNo.seatNum
            directRoute = DirectRoute()
            directRoute.totSeat = temp
            directRoute.seatMap = "".join(["0" for i in range(temp)])
            if item.departureTime < instance.arriveTime:
                directRoute.departure = item
                directRoute.destination = instance
                directRoute.save()
            elif instance.arriveTime < item.departureTime:
                directRoute.departure = instance
                directRoute.destination = item
                directRoute.save()
