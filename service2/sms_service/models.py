from django.db import models


class Room(models.Model):
    receiver = models.CharField(max_length=255)


class SMS(models.Model):
    content = models.TextField(max_length=1000, blank=True, null=False)
    date_time = models.DateTimeField(auto_now_add=True)
    sender_id = models.IntegerField(blank=True)
    sender_name = models.CharField(max_length=100, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True)
