from django import forms
from .models import CsvFile


class CsvModelForm(forms.ModelForm):
    class Meta:
        model = CsvFile
        fields = ['file_name']
