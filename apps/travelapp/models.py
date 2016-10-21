from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import re, bcrypt
from django.contrib import messages
from datetime import date

# Create your models here.
class UserManager(models.Manager):
    def register(self, data):
        error = []
        if len(data["first_name"]) < 3 or any(char.isdigit() for char in data["first_name"]):
            error.append('First name must be at least 3 characters and contain no numbers')
        if len(data["last_name"]) < 3 or any(char.isdigit() for char in data["last_name"]):
            error.append('Last name must be at least 3 characters and contain no numbers')
        if len(data["username"]) < 3:
            error.append('Username must be at least 3 char')
        if len(data["password"]) < 8:
            error.append('Password is too short')

        user = self.filter(username = data['username'])

        if user:
            error.append('username taken')
        if data['password'] != data['password_confirm']:
            error.append('please match your passwords')
        if error:
            return (False, error)

        hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user = self.create(first_name = data["first_name"],last_name = data["last_name"],username = data["username"], password = hashed)
        return (True, user)

    def login(self, data):
        error = []
        user = self.filter(username=data['username'])
        if user:
            if bcrypt.hashpw(data['password'].encode('utf-8'), user[0].password.encode('utf-8')) == user[0].password:
                return (True, user[0])
        error.append("Invalid credentials, please try again")
        return (False, error)

class TravelManager(models.Manager):
    def create_travel(self, form_data, user_id):
        #validate trip
        errors = []
        if len(form_data['destination']) < 1:
            errors.append("You must enter a destination")
        if len(form_data['description']) < 1:
            errors.append("You must enter a description")
        if len(form_data['start_date']) < 1:
            errors.append("You must enter a start date")
        if len(form_data['end_date']) < 1:
            errors.append("You must enter a end date")
        if errors:
            return(False, errors)
        else:
            TripSchedule.objects.create(usertrip=User.objects.get(id=user_id),destination=form_data['destination'], description=form_data['description'], start_date=form_data['start_date'],end_date=form_data['end_date'])
            return (True, form_data)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripSchedule(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    usertrip = models.ForeignKey(User, related_name="usertrip")
    travellers = models.ManyToManyField(User, related_name="travellers")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TravelManager()
