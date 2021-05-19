from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    room_num = models.CharField(max_length=8, blank=True)
    meeting_token = models.CharField(max_length=100, blank=True)


class Meeting(models.Model):
    appID = models.CharField(max_length=50, default="730a447ceec841d28133f2415810742b")
    certification = models.CharField(max_length=200, default="7b0418bbd36b402eb1e32f3ae7a6a646")
    channel = models.CharField(max_length=8, unique=True)
    host = models.CharField(max_length=20, unique=True)