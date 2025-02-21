import httpx
from concurrent.futures import ThreadPoolExecutor
import time

# script that performs deposit of 10,000 to user_id 12 in parallel
BASE_URL = "http://127.0.0.1:8000"
CONCURRENT_REQUESTS = 100
AMOUNT = 100
USER_ID = "12"

def get_balance(user_id):
    response = httpx.get(f"{BASE_URL}/balance/{user_id}/")
    return response.json().get("balance")

def make_deposit_request(user_id, amount):
    time.sleep(0.01)
    with httpx.Client() as client:
        response = client.post(f"{BASE_URL}/deposit/{user_id}/", json={"amount": amount})
        return response.json().get("new_balance")

def run_concurrent():   
    initial_balance = get_balance(USER_ID)
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = [
            executor.submit(make_deposit_request, USER_ID, AMOUNT) 
            for _ in range(CONCURRENT_REQUESTS)
        ]
        balances = [future.result() for future in futures]
    
    final_balance = get_balance(USER_ID) # Get final balance
    expected_balance = initial_balance + (AMOUNT * CONCURRENT_REQUESTS)
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    # Print results
    print("\nResults:")
    print(f"Execution time: {execution_time:.2f} seconds")
    print(f"Initial balance: {initial_balance}")
    print(f"New balance: {final_balance}")
    print(f"Unique balance updates: {len(set(balances))}")

if __name__ == "__main__":
    run_concurrent()