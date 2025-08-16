from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hospital, Receiver
from .models import BloodSample

# Hospital Registration Form
class HospitalRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=200)
    location = forms.CharField(max_length=200)
    specialization = forms.CharField(max_length=200)
    contact_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'location', 'specialization', 'contact_number']

# Receiver Registration Form
class ReceiverRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=200)
    blood_group = forms.ChoiceField(choices=Receiver.BLOOD_GROUPS)
    contact_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'blood_group', 'contact_number']
        
class BloodSampleForm(forms.ModelForm):
    class Meta:
        model = BloodSample
        fields = ['blood_type', 'units_available', 'location']
from django.db import models


from django import forms
from .models import RequestSample, Campaign

class RequestSampleForm(forms.ModelForm):
    class Meta:
        model = RequestSample
        fields = ['requester_name', 'contact_info']
class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'start_date', 'end_date']