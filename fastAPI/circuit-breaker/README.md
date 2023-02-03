<!-- @format -->

# Circuit Breaker Pattern (FASTAPI)

The Circuit Breaker pattern is used to prevent cascading failures in a microservices architecture. It works by using a stateful component (the circuit breaker) to monitor the success or failure of a dependent service. If the dependent service fails too many times, the circuit breaker opens and prevents further requests to that service. Once the dependent service has been restored, the circuit breaker will close and allow requests to continue.

Here's an example of how you can implement the Circuit Breaker pattern in FastAPI using Python:

```
from fastapi import FastAPI, HTTPException
from requests import get, exceptions

app = FastAPI()

@app.get("/")
def read_root():
    try:
        response = get("https://api.example.com/data")
        response.raise_for_status()
        return response.json()
    except exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Unable to connect to example.com")
```
