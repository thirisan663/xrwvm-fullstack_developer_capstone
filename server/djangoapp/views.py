# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from .models import CarMake, CarModel
from .populate import initiate
from django.contrib.auth import login, authenticate, logout
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def get_cars(request):
    count = CarMake.objects.all().count()
    print(count)

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')

    cars = []

    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})
# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)

    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        data = {
            "userName": username,
            "status": "Authenticated"
        }
    else:
        data = {
            "userName": username
        }

    return JsonResponse(data)


@csrf_exempt
def registration(request):
    data = json.loads(request.body)

    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )

        login(request, user)

        data = {
            "userName": username,
            "status": "Authenticated"
        }

        return JsonResponse(data)

    else:
        data = {
            "userName": username,
            "error": "Already Registered"
        }

        return JsonResponse(data)

@csrf_exempt
def logout_request(request):
    logout(request)  # Terminate user session
    data = {"userName": ""}
    return JsonResponse(data)