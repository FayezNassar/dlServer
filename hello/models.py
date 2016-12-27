from django.db import models


# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


# the working time average model
class TimeStatistic(models.Model):
    device_id = models.IntegerField(primary_key=True)
    mini_patch_times = models.IntegerField()
    total_time = models.FloatField()


class AccuracyStatistic(models.Model):
    epoch = models.IntegerField()
    accuracy = models.FloatField()

