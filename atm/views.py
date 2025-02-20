from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def welcome(request): # Welcome screen
    return HttpResponse("Welcome to atm")