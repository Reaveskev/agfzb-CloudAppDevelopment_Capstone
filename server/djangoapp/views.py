from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview, CarModel, CarMake
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def get_about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def get_contact(request):
    return render(request, 'djangoapp/contact.html')




# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
       
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Not sure where to send them as of now
            return redirect('djangoapp/index.html')
        else:
            # Not sure where to send them as of now
            return render(request, 'djangoapp/index.html', context)
    else:
        # Not sure where to send them as of now
        return render(request, 'djangoapp/index.html', context)




# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    # Not sure where to send them as of now
    return render(request, 'djangoapp/index.html', context)





# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
  
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:popular_course_list")
        else:
            return render(request, 'onlinecourse/user_registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context={}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/56dd4597-36e1-4f9d-ac98-a7d0245de155/dealership-package/get-dealership"

        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context["dealership_list"]=dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

