# BFF

Backend-for-Frontend service for the Continuous Multilingual Aspect Sentiment and Stance Intelligence Platform.

## Responsibility

The BFF is the public backend entry point for the frontend.

It is responsible for:

- Receiving frontend requests
- Validating input
- Generating request IDs
- Calling backend microservices
- Orchestrating the processing pipeline
- Aggregating service responses
- Returning the final response
- Handling service errors

The BFF does not contain NLP or machine-learning logic.

## Architecture

Frontend
    |
    v
BFF
    |
    +--> Multilingual + Aspect Service
    |
    +--> Sentiment + Stance Service
    |
    +--> Adaptation Service

## Default Port

8000

## API Prefix

/api/v1

## Endpoints

### Health

GET /health

### Process Text

POST /api/v1/process/text

### Process Dataset

POST /api/v1/process/dataset

### Get Result

GET /api/v1/results/{id}

### Get Results

GET /api/v1/results

## Environment Variables

MULTILINGUAL_ASPECT_SERVICE_URL
SENTIMENT_STANCE_SERVICE_URL
ADAPTATION_SERVICE_URL
SERVICE_TIMEOUT
API_PREFIX
DEBUG