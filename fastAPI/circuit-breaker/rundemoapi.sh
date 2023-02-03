#!/bin/bash

uvicorn demoapi:app --host 0.0.0.0 --port 5001 --reload