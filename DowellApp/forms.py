from django import forms
from django.core import validators
from .models import StattricksModel

class DowellData(forms.ModelForm):
    class Meta:
        model = StattricksModel
        fields = ['process_ID', 'process_sequence_ID', 'series','minimum_series', 'minimum_series_datapoint', 'minimum_continuous_datapoint','process_hours', 'values']