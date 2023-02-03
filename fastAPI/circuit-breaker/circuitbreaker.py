from fastapi import FastAPI, HTTPException
import requests
import time

app = FastAPI()

# Circuit breaker state
breaker_state = "CLOSED"
failure_count = 0
MAX_FAILURES = 5
TIMEOUT = 5

url = "http://localhost:5001/data"
headers = { "Content-Type": "application/json" }

@app.post("/create")
def create_root(item: dict):
    global breaker_state, failure_count
    if breaker_state == "OPEN":
        time.sleep(TIMEOUT)
        return {"error": "Circuit breaker is open", "state": "OPEN"}
    try:
        response = requests.post(url, headers=headers, json=item)
        response.raise_for_status()
        breaker_state = "CLOSED"
        failure_count = 0
        return {"result": response.json(), "state": "CLOSED"}
    except requests.exceptions.RequestException as e:
        failure_count += 1
        if failure_count >= MAX_FAILURES:
            breaker_state = "OPEN"
        raise HTTPException(status_code=500, detail="Unable to connect to the API")

if __name__ == '__main__':
    uvicorn.run("circuitbreaker:app", host="0.0.0.0", port=5000, reload=True, workers=2)
