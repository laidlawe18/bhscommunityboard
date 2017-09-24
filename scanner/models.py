from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    
    electronics_level = models.IntegerField(default=0)
    cad_3d_level = models.IntegerField(default=0)
    vinyl_cutting_level = models.IntegerField(default=0)
    printing_3d_level = models.IntegerField(default=0)
    sewing_level = models.IntegerField(default=0)
    video_editing_level = models.IntegerField(default=0)
    cad_2d_level = models.IntegerField(default=0)
    
    hours = models.FloatField(default=0)
    
class LeadershipMember(Person):
    user = models.OneToOneField(User, default=0)
    periods = models.CharField(max_length=18)
    can_add_leadership_members = models.BooleanField(default=False)
    can_change_leadership_permissions = models.BooleanField(default=False)
    
    
class CheckoutItem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    default_checkout_time = models.IntegerField()
    
class Checkin(models.Model):
    person = models.ForeignKey(Person)
    checkin = models.DateTimeField()
    checkout = models.DateTimeField()
    completed = models.BooleanField(default=False)

class Checkout(models.Model):
    person = models.ForeignKey(Person)
    item = models.ForeignKey(CheckoutItem)
    date_checked_out = models.DateTimeField()
    date_due = models.DateTimeField()
    
    date_returned = models.DateTimeField(default=datetime(1, 1, 1))
    checked_in = models.BooleanField(default=False)

class ScheduleDay(models.Model):
    day_off = models.BooleanField(default=False)
    date = models.DateField()
    day = models.IntegerField()
    schedule = models.CharField(max_length=7)

class Period(models.Model):
    period_letter = models.CharField(max_length=5) # 0 for A, 1 for B, etc.
    day = models.ForeignKey(ScheduleDay)
    period_number = models.IntegerField()
    individual_spots = models.IntegerField(default=15)
    
    def __str__(self):
        return self.period_letter
    
class PeriodPerson(models.Model):
    person = models.ForeignKey(Person)
    period = models.ForeignKey(Period)

class PeriodClass(models.Model):
    teacher = models.ForeignKey(Person)
    period = models.ForeignKey(Period)
    students = models.IntegerField()


    
