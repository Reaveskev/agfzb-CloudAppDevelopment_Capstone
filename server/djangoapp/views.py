from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview, CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
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
    # url = "https://us-south.functions.appdomain.cloud/api/v1/web/56dd4597-36e1-4f9d-ac98-a7d0245de155/dealership-package/get-dealership"
    # dealerships = get_dealers_from_cf(url)
    # # Concat all dealer's short name
    # context["dealership_list"]=dealerships
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['pword']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            # If not, return to login page again
            context["message"]="Username or password is incorrect."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)




# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    # url = "https://us-south.functions.appdomain.cloud/api/v1/web/56dd4597-36e1-4f9d-ac98-a7d0245de155/dealership-package/get-dealership"
    # dealerships = get_dealers_from_cf(url)
    # Concat all dealer's short name
    # context["dealership_list"]=dealerships
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return render(request, 'djangoapp/index.html', context)





# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pword']
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
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships

def get_dealerships(request):
    if request.method == "GET":
        context={}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/56dd4597-36e1-4f9d-ac98-a7d0245de155/dealership-package/get-dealership"

        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context["dealership_list"]=dealerships
        # # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)
        
        


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context={}
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/56dd4597-36e1-4f9d-ac98-a7d0245de155/dealership-package/get-reviews"
    # Get dealers from the URL
    
    dealer_details = get_dealer_reviews_from_cf(url, dealer_id)

    context["dealer_id"]=dealer_id
    context["reviews"]=dealer_details
    return render(request, 'djangoapp/dealer_details.html', context)



# # Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    # If it is a GET request, just render the add_review page
    if request.method == 'GET':
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/56dd4597-36e1-4f9d-ac98-a7d0245de155/dealership-package/get-dealership"
        # Get dealers from the URL
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[dealer_id-1].full_name,
            "cars": CarModel.objects.all()
        }
       
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if (request.user.is_authenticated):
            review = dict()
            review["id"]=0
            review["name"]=request.POST["name"]
            review["dealership"]=dealer_id
            review["review"]=request.POST["content"]
            if ("purchasecheck" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
            if review["purchase"] == True:
                car_parts=request.POST["car"].split("|")
                review["purchase_date"]=request.POST["purchase_date"] 
                review["car_make"]=car_parts[0]
                review["car_model"]=car_parts[1]
                review["car_year"]=car_parts[2]

            else:
                review["purchase_date"]=None
                review["car_make"]=None
                review["car_model"]=None
                review["car_year"]=None
            json_data = json.dumps(review)
            json_result = post_request("https://us-south.functions.appdomain.cloud/api/v1/web/56dd4597-36e1-4f9d-ac98-a7d0245de155/dealership-package/post-review", json_data, dealerId=dealer_id)

            if "error" in json_result:
                context["message"] = "ERROR: Review was not submitted."
            else:
                context["message"] = "Review was submited"
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
