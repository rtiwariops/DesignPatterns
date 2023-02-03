<!-- @format -->

# Circuit Breaker Pattern (FASTAPI)

The Circuit Breaker pattern is used to prevent cascading failures in a microservices architecture. It works by using a stateful component (the circuit breaker) to monitor the success or failure of a dependent service. If the dependent service fails too many times, the circuit breaker opens and prevents further requests to that service. Once the dependent service has been restored, the circuit breaker will close and allow requests to continue.

## DemoAPI

Here's an example of how you can implement the Circuit Breaker pattern in FastAPI using Python:

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str

@app.post("/data")
async def create_item(item: Item):
    return {"name": item.name, "description": item.description}

if __name__ == '__main__':
    uvicorn.run("demoapi:app", host="0.0.0.0", port=5001, reload=True, workers=2)
```

## Circuit Breaker Code

I have include a stateful circuit breaker by adding a counter for failed requests and an if statement that opens the circuit breaker after a certain number of failures. For example:

```
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
```

This code is creating a FastAPI web service that acts as a circuit breaker pattern when connecting to an external API service running on "http://localhost:5001/data". The circuit breaker pattern allows the service to handle potential failures in communication with the external API.

When a POST request is made to the "/create" endpoint of the service, it sends a request to the external API with the given "item" data. If the external API response is successful, the response is returned with the "result" key and the breaker state is set to "CLOSED". If the external API response fails, the failure count is incremented and if the failure count exceeds the defined maximum failures (MAX_FAILURES), the breaker state is set to "OPEN". If the breaker state is "OPEN", the service will wait for a defined timeout (TIMEOUT) and return an error message with the breaker state. If the external API response fails and the breaker state is not "OPEN", an HTTPException with a status code of 500 is raised and the error message "Unable to connect to the API" is returned.
