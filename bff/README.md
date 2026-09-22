# BFF — Backend for Frontend

The BFF is the single backend entry point for the Multilingual Intelligence Platform frontend.

It does not perform NLP or machine learning.

Its responsibility is to orchestrate:

Frontend
    ↓
BFF
    ↓
Service 1 — Multilingual + Aspect
    ↓
Service 2 — Sentiment + Stance
    ↓
BFF
    ↓
Service 3 — Adaptation
    ↓
BFF
    ↓
Frontend

## Port

BFF runs on:

http://localhost:8000

## Services

Service 1:

http://localhost:8001

Service 2:

http://localhost:8002

Service 3:

http://localhost:8003

## Endpoints

### POST /process

Main processing endpoint.

Request:

{
  "request_id": "req_12345678",
  "text": "The camera quality is excellent but battery life is poor."
}

The BFF sends the request through all required services and returns the combined result.

### GET /health

Checks whether the BFF is running.

## Project Structure

bff/
├── app.py
├── config.py
├── routes.py
├── views.py
├── pipeline.py
├── service1_client.py
├── service2_client.py
├── service3_client.py
├── requirements.txt
├── .env.example
└── README.md

## Responsibilities

### app.py

Starts the Flask application.

### config.py

Contains BFF and service configuration.

### routes.py

Defines HTTP routes.

### views.py

Handles incoming HTTP requests and outgoing HTTP responses.

### pipeline.py

Coordinates the complete Service 1 → Service 2 → Service 3 workflow.

### service1_client.py

Communicates with Service 1.

### service2_client.py

Communicates with Service 2.

### service3_client.py

Communicates with Service 3.

## Important Rule

The BFF must not contain:

- language detection
- aspect extraction
- sentiment calculation
- stance calculation
- model training
- model inference
- NLP preprocessing

Those responsibilities belong to the individual services.

The BFF only:

Receive → Call → Pass → Combine → Call → Return