from django.db import models
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300,primary_key=True)
    latitude = models.FloatField(blank=False)
    longitude =models.FloatField(blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    notice = models.TextField(blank=True)
    spec = models.TextField(blank=True)


    def created(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class SeatInfo(models.Model):
        room = models.ForeignKey(Room,on_delete=models.CASCADE,null=True)
        data = models.TextField(blank=True)
        seatImage = models.ImageField(blank=True)
        created_date = models.DateTimeField(default=timezone.now)

        def __str__(self):
            return (self.room + " "+ self.created_date)
