from django.shortcuts import render
from .forms import DowellData
from .models import StattricksModel

# Create your views here.
def start():
    series = [1, 2, 3]
    minimum_series = [1, 2, 3]
    minimum_series_datapoint = [1, 2, 3]
    for a,b,c in series, minimum_series, minimum_series_datapoint:
        dowellstattricks(1, 2, a, b, c, 6, "yes", 4)

def dowellstattricks(processID,process_sequence_ID,series,minimum_series,minimum_series_datapoint,minimum_continuous_datapoint,process_hours,values):
    save_data=StattricksModel(processID=processID,process_sequence_ID=process_sequence_ID,series=series,minimum_series=minimum_series,minimum_series_datapoint=minimum_series_datapoint,minimum_continuous_datapoint=minimum_continuous_datapoint,process_hours=process_hours,values=values)
    save_data.save()


