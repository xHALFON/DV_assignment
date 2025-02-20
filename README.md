# ATM System

A simple ATM system implemented in Django with thread-safe operations.

## Features
- Get account balance
- Deposit money
- Withdraw money
- Thread-safe operations with locks
- Concurrent operation testing

## Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python manage.py runserver
   ```
   Run the server with docker:
   ```bash
   docker build -t atm_server .

   docker run -p 8000:8000 atm_server
   ```

## Testing
Run the tests with:
```bash
pytest tests/test_atm.py
pytest -s tests/threadSafe_test.py
```
or:
```bash
pytest -s
```

## API Endpoints
- `GET /` - Welcome message
- `GET /balance/<user_id>/` - Get user balance
- `POST /deposit/<user_id>/` - Deposit money
- `POST /withdraw/<user_id>/` - Withdraw money

## Example Usage
```bash
# Get balance
curl http://localhost:8000/balance/123/

# Deposit
curl -X POST http://localhost:8000/deposit/123/ ^ -H "Content-Type: application/json" ^ -d "{\"amount\": 100}"

# Withdraw
curl -X POST http://localhost:8000/withdraw/123/ ^ -H "Content-Type: application/json" ^ -d "{\"amount\": 50}"