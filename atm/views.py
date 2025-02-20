from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

users_balance = {} #Save users balance

def is_valid_user_id(user_id): #Check if the user_id is number
    return user_id.isdigit()

@csrf_exempt
def get_balance(request, user_id): # Get balance from user
    if not is_valid_user_id(user_id):
        return JsonResponse({"err": "Invalid user_id. Only numbers allowed"}, status=400)
    
    if request.method != "GET": #Check if the method is get
        return JsonResponse({"err": "Invalid request method"}, status=405)
    
    try:
        balance = users_balance.get(user_id, 0) # Fetch the user balance
        return JsonResponse({"user_id": user_id, "balance": balance, "dict": users_balance})
    except Exception as e:
        return JsonResponse({"err": str(e)}, status=400)

@csrf_exempt
def welcome(request): # Welcome screen
    return HttpResponse("Welcome to atm")