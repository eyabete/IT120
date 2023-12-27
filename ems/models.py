from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.enums import Choices


class Participant(models.Model):
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True)
    profile_pic = models.ImageField(null=True, blank=True, default="profile_1.png")
    dob = models.DateField(null=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Organiser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    about = models.TextField(max_length=600, null=True)
    location = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)


class Event(models.Model):
    CATEGORIES = [
        ('Conference', 'Conference'),
        ('Party', 'Party'),
        ('Seminar', 'Seminar'),
        ('Concert', 'Concert'),
    ]
    name = models.CharField(max_length=200)
    organiser = models.ForeignKey(Organiser, null=True, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, null=True)
    category = models.CharField(max_length=200, choices=CATEGORIES)
    event_date = models.DateField()
    created_dated = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    
class Transaction(models.Model):
    participant = models.ForeignKey(Participant, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    date = models.DateField()
    amount = models.IntegerField()


class Cancellation(models.Model):
    participant = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now_add=True)
    reason = models.CharField(max_length=200, null=True)


class Advertisement(models.Model):
    DURATIONS = [
        (2, 2),
        (6, 6),
        (12, 12),
        (24, 24),
        (48, 48)
    ]
    event = models.ForeignKey(Event, on_delete=CASCADE)
    duration = models.IntegerField(default=2, choices=DURATIONS)

    def getEvent(self):
        return self.event


class Item(models.Model):
    CATEGORIES = [
        ('T-Shirt', 'T-Shirt'),
        ('Coffee Mug', 'Coffee Mug'),
        ('Stickers', 'Sticker'),
        ('Backpack', 'Backpack'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, choices=CATEGORIES) 
    organiser = models.ForeignKey(Organiser, max_length=200, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Shipper(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Shipment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)


class Registration(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reg_date = models.DateField(auto_now_add=True)
    
class EventEvaluation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 5)])