#!/bin/bash

uvicorn circuitbreaker:app --host 0.0.0.0 --port 5000 --reload