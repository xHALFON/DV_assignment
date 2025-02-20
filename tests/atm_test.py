import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"  # Server_url

def test_welcome(): # Check welcome endpoint
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.text == "Welcome to atm"

def test_deposit(): # Check deposit endpoint
    user_id = "123"
    deposit_data = {"amount": 100.0}

    balance_response = requests.get(f"{BASE_URL}/balance/{user_id}/")
    user_balance = balance_response.json().get("balance") # take the current user balance
    
    response = requests.post(f"{BASE_URL}/deposit/{user_id}/", json=deposit_data)
    assert response.status_code == 200
    assert response.json()["new_balance"] == user_balance + deposit_data["amount"] # check if the deposit is correct

def test_withdraw(): # Check withdraw endpoint
    user_id = "123"
    withdraw_data = {"amount": 50.0}
    
    balance_response = requests.get(f"{BASE_URL}/balance/{user_id}/")
    user_balance = balance_response.json().get("balance") # take the current user balance
    
    response = requests.post(f"{BASE_URL}/withdraw/{user_id}/", json=withdraw_data)
    assert response.status_code == 200
    assert response.json()["new_balance"] == user_balance - withdraw_data["amount"] # check if the withdraw is correct

def test_insufficient_funds(): # Check withdraw when there is not enough amount
    user_id = "123"
    withdraw_data = {"amount": 10000.0}
    
    response = requests.post(f"{BASE_URL}/withdraw/{user_id}/", json=withdraw_data)
    assert response.status_code == 400
    assert response.json()["err"] == "Insufficient funds"