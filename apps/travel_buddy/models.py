# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
    def new_user_validator(self, post_data):
        errors = {}
        try:
            User.objects.get(user_name = post_data['user_name'])
            errors['already_user'] = 'Sorry, that user name is not available.  Please select a different user name'
        except:
            pass
        if len(post_data['name']) < 3 or len(post_data['user_name']) < 3:
            errors['name_length'] = 'Name and User Name must both be at least 3 characters'
        if len(post_data['password']) < 8:
            errors['password_length'] = 'Password should be at least 8 characters'
        if post_data['password'] != post_data['confirm']:
            errors['password_match'] = 'Passwords do not match'
        return errors

    def login_validator(self, post_data):
        errors = {}
        try:
            user = User.objects.get(user_name=post_data['user_name'])
        except:
            errors['user_not_registered'] = 'Sorry, that user name is not registered.  Please register an account.'
            return errors
        entered_pw = post_data['password']
        user_hash = user.password_hash
        if not bcrypt.checkpw(entered_pw.encode(), user_hash.encode()):
            errors['incorrect_password'] = 'Password incorrect.  Please try again!'
        return errors
    
class TripManager(models.Manager):
    def trip_validator(self, post_data):
        errors = {}
        for field in post_data:
            if len(post_data[field]) == 0:
                errors['required'] = 'All fields are required'
                return errors
        start_date = datetime.strptime(post_data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(post_data['end_date'], '%Y-%m-%d')
        if start_date <= datetime.now():
            errors['trip_start'] = 'Trip must start at a future date.'
        if end_date <= start_date:
            errors['trip_end'] = 'Trip must end at a date after it starts.'
        return errors

class User(models.Model):
    name = models.CharField(max_length=256)
    user_name = models.CharField(max_length=32)
    password_hash = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    creator = models.ForeignKey(User, related_name='created_trips')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='trips')
    objects = TripManager()
