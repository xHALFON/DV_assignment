import pytest
import httpx
from concurrent.futures import ThreadPoolExecutor
import time

BASE_URL = "http://127.0.0.1:8000"
CONCURRENT_REQUESTS = 100
AMOUNT = 100
USER_ID = "12"

def test_concurrent_deposits():
    initial_balance = get_balance(USER_ID)

    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(make_deposit_request, USER_ID, AMOUNT) for _ in range(CONCURRENT_REQUESTS)]
        balances = [future.result() for future in futures]

    final_balance = get_balance(USER_ID)
    expected_balance = initial_balance + AMOUNT * CONCURRENT_REQUESTS

    assert len(set(balances)) == CONCURRENT_REQUESTS, (
        f"Expected {CONCURRENT_REQUESTS} unique balances, got {len(set(balances))}. Possible race condition detected."
    )

    assert final_balance == expected_balance, (
        f"Expected final balance: {expected_balance}, Actual balance: {final_balance}"
    )


def get_balance(user_id):
    response = httpx.get(f"{BASE_URL}/balance/{user_id}/")
    return response.json().get("balance")

def make_deposit_request(user_id, amount=1):
    time.sleep(0.01)  # Simulate processing delay
    with httpx.Client() as client:
        response = client.post(f"{BASE_URL}/deposit/{user_id}/", json={"amount": amount})
        return response.json().get("new_balance")