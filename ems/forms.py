from django.db.models.base import Model
from django.forms import ModelForm
from django.forms import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class OrganiserForm(ModelForm):
    class Meta:
        model = Organiser
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
        exclude = ('user',)


class OrganiserForm(ModelForm):
    class Meta:
        model = Organiser
        fields = '__all__'
        exclude = ('user',)


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'


class ShipperForm(ModelForm):
    class Meta:
        model = Shipper
        fields = '__all__'


class RegistrationForm(ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'


class ShipmentForm(ModelForm):
    class Meta:
        model = Shipment
        fields = '__all__'
        

class EventEvaluationForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    rating = forms.IntegerField(label='Rating', min_value=1, max_value=5)
