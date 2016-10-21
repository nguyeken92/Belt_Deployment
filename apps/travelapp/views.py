from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import User, TripSchedule

def index(request):
    return render(request, 'travelapp/index.html')

def register(request): #just taking the request object
    user = User.objects.register(request.POST) #user = a tuple, 2 options, (True, user) or (False, errors)
    if user[0]:
        request.session['user'] = {
            'id':user[1].id,
            'first_name':user[1].first_name,
            'last_name':user[1].last_name,
            'username':user[1].username,
        }
        return redirect(reverse('travel:home'))
    #build flash messages here using user[1]
    for error in user[1]: #always going to be referring as user 1 because it's the first user in the list
        messages.error(request, error)
    return redirect(reverse('travel:index'))

def login(request):
    user = User.objects.login(request.POST)
    if user[0]:
        request.session['user'] = {
            'id':user[1].id,
            'first_name':user[1].first_name,
            'last_name':user[1].last_name,
            'username':user[1].username,
        }
        return redirect(reverse('travel:home')) #what this does here is when the log in is successful, it will redirect the user to the home page of the bookreview app
 #flash messages
    for error in user[1]:
        messages.error(request, error)
    return redirect(reverse('travel:index'))

def logoff(request):
    request.session.clear()
    return redirect(reverse('travel:index'))

def home(request):
    user = User.objects.get(id=request.session['user']['id'])
    context={
        'trips_on':TripSchedule.objects.filter(usertrip=user)|TripSchedule.objects.filter(travellers__id=user.id), #what this does is it will get all of the objects in the tripschedule table, and filter it based on the foreign key from the table and get that specific user
        'trips_off':TripSchedule.objects.exclude(usertrip=user).exclude(travellers__id=user.id)
    }
    return render(request, 'travelapp/home.html', context)

def add(request):
    return render(request, 'travelapp/add.html')

def create(request):
    result = TripSchedule.objects.create_travel(request.POST, request.session['user']['id'])
    if result[0]:
        return redirect(reverse('travel:home'))
    elif result[0] == False:
        errors = result[1]
        for error in errors:
            messages.error(request, error)
        return redirect(reverse('travel:add'))

def show(request, travel_id):
    context = {
        'trip':TripSchedule.objects.get(id=travel_id),
    }
    return render(request,'travelapp/show.html', context)

def join(request, id):
    trip = TripSchedule.objects.get(id=id)
    user = User.objects.get(id=request.session['user']['id'])
    trip.travellers.add(user)
    return redirect(reverse('travel:home'))
