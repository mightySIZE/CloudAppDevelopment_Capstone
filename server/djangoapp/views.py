from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    if request.method == "GET":
        logout(request)
        return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
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
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        # Construct the path to the dealerships.json file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join('/Users/mo/Desktop/CloudAppDevelopment_Capstone/cloudant/data/dealerships.json')

        # Read the dealerships data from the JSON file
        with open(file_path, "r") as file:
            json_data = json.load(file)

        # Parse JSON data into a CarDealer object list
        dealerships = []
        for dealer_doc in json_data["dealerships"]:
            dealer_obj = CarDealer(
                #_id = dealer_doc["_id"],
                #_rev = dealer_doc["_rev"],
                state = dealer_doc["state"],
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"],
            )
            dealerships.append(dealer_obj)
        context = {
            'dealerships': dealerships
        }

        # Render the index.html template with the context
        return render(request, 'djangoapp/index.html', context)

        # # Concat all dealer's short name
        # dealer_names = " ".join([dealer.short_name for dealer in dealerships])
        # # Return a list of dealer short name
        # return HttpResponse(dealer_names)
    


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        # Define the URL for getting dealer reviews from the cloud function

        # Get dealer reviews from the cloud function using the dealer_id
        dealer_reviews = get_dealer_reviews_from_cf(dealer_id)

        # Get the dealer object from the database using the dealer_id
        dealer = CarDealer.objects.get(id=dealer_id)

        # Create a context dictionary containing the dealer and dealer_reviews
        context = {
            "dealer": dealer,
            "dealer_reviews": dealer_reviews,
        }

        # Render the dealer_details.html template with the context
        return render(request, "djangoapp/dealer_details.html", context)



# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

