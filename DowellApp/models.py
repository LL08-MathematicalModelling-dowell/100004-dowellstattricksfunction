from django.db import models

# Create your models here.
class StattricksModel(models.Model):
    request_number=models.IntegerField()
    process_ID = models.IntegerField()
    process_sequence_ID = models.IntegerField()
    series = models.IntegerField()
    minimum_series = models.IntegerField()
    minimum_series_datapoint = models.IntegerField()
    minimum_continuous_datapoint = models.IntegerField()
    process_hours = models.CharField(max_length=100)
    values = models.IntegerField()