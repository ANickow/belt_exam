# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
# reverse with named spaces
from django.core.urlresolvers import reverse
# flash messages
from django.contrib import messages
# password encryption
import bcrypt
from datetime import datetime
from models import User, Trip

def index(request):
    return render(request, 'travel_buddy/index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.new_user_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            request.session['message_location']='registration'
            return redirect(reverse('index'))
        else:
            name = request.POST['name']
            user_name = request.POST['user_name']
            password = request.POST['password']
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            new_user = User.objects.create(name=name, user_name=user_name, password_hash=password_hash)
            user_id = new_user.id
            request.session['logged_in_id']=user_id
            return redirect(reverse('home'))
    else:
        return redirect(reverse('index'))

def authenticate(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            request.session['message_location']='login'
            return redirect(reverse('index'))
        else:
            user_name = request.POST['user_name']
            user = User.objects.get(user_name=user_name)
            user_id = user.id
            request.session['logged_in_id']=user_id
            return redirect(reverse('home'))
    else:
        return redirect(reverse('index'))

def home(request):
    user = User.objects.get(id = request.session['logged_in_id'])
    user_trips = user.trips.all()
    trips = Trip.objects.all()
    other_trips = []
    for trip in trips:
        user_on_trip = False
        participants = trip.users.all()
        for participant in participants:
            if participant.id == user.id:
                user_on_trip = True
        if not user_on_trip:
            other_trips.append(trip)
    context = {
        'user' : user,
        'user_trips' : user_trips,
        'other_trips' : other_trips
    }
    request.session['page']='home'
    return render(request, 'travel_buddy/dashboard.html', context)

def read_destination(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    participants = trip.users.all()
    trip_users = []
    for participant in participants:
        if participant.id != trip.creator.id:
            trip_users.append(participant)
    context = {
        'trip': trip,
        'trip_users': trip_users
    }
    request.session['page']='destination'
    return render(request, 'travel_buddy/destination.html', context)

def add(request):
    request.session['page']='add'
    return render(request, 'travel_buddy/add.html')

def create(request):
    if request.method == 'POST':
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect(reverse('add'))
        else:
            destination = request.POST['destination']
            description = request.POST['description']
            start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
            user_id = request.session['logged_in_id']
            user = User.objects.get(id=user_id)
            trip = Trip.objects.create(destination=destination, description=description, start_date=start_date, end_date=end_date, creator = user)
            trip.users.add(user)
            return redirect(reverse('home'))
    else:
        return redirect(reverse('add'))

def join(request, trip_id):
    user_id = request.session['logged_in_id']
    user = User.objects.get(id=user_id)
    trip = Trip.objects.get(id=trip_id)
    trip.users.add(user)
    return redirect(reverse('home'))

def logout(request):
    request.session.clear()
    return redirect(reverse('index'))