from django.db import models


# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class MaxClientID(models.Model):
    max_id_str = models.CharField(primary_key=True, max_length=20)
    max_id = models.IntegerField()


# the working time average model
class TimeStatistic(models.Model):
    device_id = models.IntegerField(primary_key=True)
    mini_patch_times = models.IntegerField()
    total_time = models.FloatField()


class AccuracyStatistic(models.Model):
    epoch_number = models.IntegerField(primary_key=True)
    accuracy = models.FloatField()
    number_of_validate_post = models.IntegerField()

