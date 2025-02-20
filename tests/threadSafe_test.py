import pytest
import httpx
from concurrent.futures import ThreadPoolExecutor
import time

BASE_URL = "http://127.0.0.1:8000"
NUM_REQUESTS = 100
WORKER_DELAY = 0.01  # Add a small delay to make race conditions more likely

def make_deposit_request(user_id): # Make deposit of 1 and return new balance
    time.sleep(WORKER_DELAY)  # Add delay to simulate longer processing
    with httpx.Client() as client:
        response = client.post(
            f"{BASE_URL}/deposit/{user_id}/",
            json={"amount": 1}
        )
        return response.json().get("new_balance")

def test_concurrent_deposits():
    user_id = "12"
    
    # Check the balance of the user at the beginning
    initial_response = httpx.get(f"{BASE_URL}/balance/{user_id}/")
    initial_balance = initial_response.json().get("balance")
    print(f"Initial balance: {initial_balance}")
    
    # Use ThreadPoolExecutor to create real concurrent requests
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = [
            executor.submit(make_deposit_request, user_id)
            for _ in range(NUM_REQUESTS)
        ]
        balances = [future.result() for future in futures]
    
    # Get the final balance
    final_response = httpx.get(f"{BASE_URL}/balance/{user_id}/")
    final_balance = final_response.json().get("balance")
    expected_balance = initial_balance + NUM_REQUESTS # The expected balance at the end
    
    print(f"All recorded balances: {sorted(balances)}")
    print(f"Final balance: {final_balance}")
    print(f"Expected balance: {expected_balance}")
    print(f"Unique balance values: {len(set(balances))}")
    
    # If there's no race condition, we should see NUM_REQUESTS different balance values.
    assert len(set(balances)) == NUM_REQUESTS, \
        f"Expected {NUM_REQUESTS} unique balances, got {len(set(balances))}. This indicates a race condition."
    
    assert final_balance == expected_balance, \
        f"Expected final balance: {expected_balance}, Actual balance: {final_balance}"