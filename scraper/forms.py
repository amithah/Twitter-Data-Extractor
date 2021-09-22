from django import forms
from .models import Job
from django.forms import ModelForm

# ref:https://pypi.org/project/django-tempus-dominus/
from tempus_dominus.widgets import DateTimePicker
from datetime import datetime


class JobForm(ModelForm):
    # since = forms.DateTimeField(
    #     widget=DateTimePicker(
    #         options={
    #             'useCurrent': True,
    #             'collapse': False,
    #             'maxDate': datetime.strftime(datetime.now(), "%Y-%m-%d "),
    #             'format': 'YYYY-MM-DD HH:mm:ss',
    #         },
    #
    #         attrs={
    #             'append': 'fa fa-calendar',
    #             'icon_toggle': True,
    #
    #         }
    #     ),
    #     help_text="Starting date",
    # )
    # until = forms.DateTimeField(
    #     widget=DateTimePicker(
    #         options={
    #             'useCurrent': True,
    #             'collapse': False,
    #             'maxDate': datetime.strftime(datetime.now(), "%Y-%m-%d "),
    #             'format': 'YYYY-MM-DD HH:mm:ss',
    #
    #         },
    #
    #         attrs={
    #             'append': 'fa fa-calendar',
    #             'icon_toggle': True,
    #         }
    #     ),
    #     help_text="End date",
    # )

    class Meta:
        model = Job
        fields = ('keyword','limit','language','verified','output_type')

