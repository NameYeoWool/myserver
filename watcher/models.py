from django.db import models
from django.utils import timezone



class Room(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300,primary_key=True)
    latitude = models.FloatField(blank=False)
    longitude =models.FloatField(blank=False)
    contact = models.BooleanField(default=False,help_text="가맹점일 경우 체크하시오.")
    created_date = models.DateTimeField(default=timezone.now)
    notice = models.TextField(blank=True)
    spec = models.TextField(blank=True)


    def created(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class SeatInfo(models.Model):
        room = models.ForeignKey(Room,on_delete=models.CASCADE)
        data = models.TextField(blank=True)
        seatImage = models.ImageField(blank=True,upload_to="seat_images/")
        created_date = models.DateTimeField(default=timezone.now)

        def __str__(self):
            return ("%s %s " %(self.room.name, self.created_date) )
