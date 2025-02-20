from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import threading

users_balance = {} #Save users balance
lock = threading.Lock() # lock critical section

def is_valid_user_id(user_id): #Check if the user_id is number
    return user_id.isdigit()

@csrf_exempt
def get_balance(request, user_id): # Get balance from user
    if not is_valid_user_id(user_id):
        return JsonResponse({"err": "Invalid user_id. Only numbers allowed"}, status=400)
    
    if request.method != "GET": #Check if the method is get
        return JsonResponse({"err": "Invalid request method"}, status=405)
    
    try:
        with lock: # Prevent race condition
            balance = users_balance.get(user_id,0) # Fetch the user balance
            return JsonResponse({"user_id": user_id, "balance": balance, "dict": users_balance})
    except Exception as e:
        return JsonResponse({"err": str(e)}, status=400)

@csrf_exempt
def deposit(request, user_id): # Deposit to user
    if not is_valid_user_id(user_id):
        return JsonResponse({"err": "Invalid user_id. Only numbers allowed"}, status=400)
        
    if request.method != "POST":
        return JsonResponse({"err": "Invalid request method"}, status=405)
    
    try:
        data = json.loads(request.body)
        amount = float(data.get("amount", 0)) # Cast to float
        
        with lock: # Prevent race condition
            if amount <= 0: # Check if the amount is legal
                return JsonResponse({"err": "Invalid deposit amount"}, status=400)
            users_balance[user_id] = users_balance.get(user_id, 0) + amount # Update the dict to the new balance
            print(f"user {user_id} new balance: {users_balance[user_id]}")
            return JsonResponse({"user_id": user_id, "new_balance": users_balance[user_id], "dict": users_balance})

    except (ValueError, json.JSONDecodeError):
        return JsonResponse({"err": "Invalid JSON data"}, status=400)

@csrf_exempt
def withdraw(request, user_id): # Withdraw from user
    if not is_valid_user_id(user_id):
        return JsonResponse({"err": "Invalid user_id. Only numbers allowed"}, status=400)
    
    if request.method != "POST":
        return JsonResponse({"err": "Invalid request method"}, status=405)
    
    try:
        data = json.loads(request.body)
        amount = float(data.get("amount", 0)) # Cast to float

        with lock: # Prevent race condition
            if amount <= 0: # check if the amount is valid
                return JsonResponse({"err": "Invalid withdrawal amount"}, status=400)
            
            if users_balance.get(user_id, 0) < amount: # Check if user has enough money
                print(f"user {user_id}: Insuffiecient funds")
                return JsonResponse({"err": "Insufficient funds"}, status=400)

            users_balance[user_id] -= amount # Update the dict to the new balance
            print(f"user {user_id} new balance: {users_balance[user_id]}")
            return JsonResponse({"user_id": user_id, "new_balance": users_balance[user_id], "dict": users_balance})

    except (ValueError, json.JSONDecodeError):
        return JsonResponse({"err": "Invalid JSON data"}, status=400)

@csrf_exempt
def welcome(request): # Welcome screen
    return HttpResponse("Welcome to atm")