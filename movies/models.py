from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Movie(models.Model):
    name = models.CharField(max_length = 255)
    image = models.ImageField(upload_to = "movies/")
    title = models.CharField(max_length=200,default="Default Movie")
    rating = models.FloatField(default=0)
    cast = models.TextField()
    description = models.TextField(blank = True,null = True) #optional

    genre = models.CharField(max_length=100,blank=True,null=True)
    language =models.CharField(max_length=100,blank=True,null=True)

    trailer_url = models.URLField(blank = True , null = True)

    def __str__(self):
        return self.name
    
class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name = 'theaters')
    time = models.DateTimeField()

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'
    
class Seat(models.Model):
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE,related_name = 'seats')
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'
    
class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.username} - {self.movie.name} - Seat{self.seat.seat_number}"




