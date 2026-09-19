# System Folder Structure

## Overview

The **Multilingual Intelligence Platform** follows a strictly service-isolated architecture. The system consists of four independently deployable Flask applications:

1. **BFF** – Backend-for-Frontend
2. **Multilingual + Aspect Service**
3. **Sentiment + Stance Service**
4. **Adaptation Service**

Each service is self-contained and maintains its own application code, configuration, models, modules, dependencies, and documentation.

## Project Structure

```text
Multilingual-Intelligence-Platform/
│
├── bff/
├── multilingual-aspect-service/
├── sentiment-stance-service/
├── adaptation-service/
├── docs/
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## 1. BFF

The `bff/` directory contains the Backend-for-Frontend service.

```text
bff/
├── app.py
├── config.py
├── models/
│   └── base_models.py
├── modules/
│   ├── process/
│   │   ├── routes.py
│   │   ├── views.py
│   │   └── models.py
│   └── results/
│       ├── routes.py
│       ├── views.py
│       └── models.py
├── requirements.txt
└── README.md
```

The BFF receives requests from the frontend, communicates with backend services through HTTP APIs, aggregates their responses, and returns the final response to the frontend.

The BFF does not contain NLP or machine-learning implementation.

## 2. Multilingual + Aspect Service

The `multilingual-aspect-service/` directory handles multilingual text processing and aspect-related operations.

```text
multilingual-aspect-service/
├── app.py
├── config.py
├── models/
│   └── base_models.py
├── modules/
│   ├── preprocessing/
│   │   ├── routes.py
│   │   └── views.py
│   ├── language_detection/
│   │   ├── routes.py
│   │   └── views.py
│   ├── aspect_extraction/
│   │   ├── routes.py
│   │   └── views.py
│   └── aspect_categorization/
│       ├── routes.py
│       └── views.py
├── requirements.txt
└── README.md
```

Its processing flow is:

```text
Input Text
    ↓
Preprocessing
    ↓
Language Detection
    ↓
Aspect Extraction
    ↓
Aspect Categorization
    ↓
Output
```

This service does not import code from the other services.

## 3. Sentiment + Stance Service

The `sentiment-stance-service/` directory handles sentiment and stance analysis.

```text
sentiment-stance-service/
├── app.py
├── config.py
├── models/
│   └── base_models.py
├── modules/
│   ├── sentiment/
│   │   ├── routes.py
│   │   ├── views.py
│   │   └── models.py
│   └── stance/
│       ├── routes.py
│       ├── views.py
│       └── models.py
├── requirements.txt
└── README.md
```

Its main responsibilities are:

* Sentiment prediction
* Stance prediction
* Returning analysis results through HTTP APIs

The service is independently deployable and does not directly import the multilingual/aspect or adaptation service.

## 4. Adaptation Service

The `adaptation-service/` directory manages continual adaptation-related functionality.

```text
adaptation-service/
├── app.py
├── config.py
├── models/
│   └── base_models.py
├── modules/
│   ├── data_integration/
│   │   ├── routes.py
│   │   ├── views.py
│   │   └── models.py
│   ├── memory/
│   │   ├── routes.py
│   │   ├── views.py
│   │   └── models.py
│   └── versioning/
│       ├── routes.py
│       ├── views.py
│       └── models.py
├── requirements.txt
└── README.md
```

The service provides the foundation for:

* New data integration
* Memory/replay management
* Model or system version management
* Future continual-learning and LoRA adaptation functionality

## 5. Service-Level `models/`

Every service may contain its own:

```text
models/
└── base_models.py
```

These models belong exclusively to that service.

There is intentionally **no root-level shared `models/` directory**.

## 6. Module Structure

Functional modules generally follow:

```text
module/
├── routes.py
├── views.py
└── models.py
```

### `routes.py`

Defines the Flask HTTP routes and connects them to the appropriate view functions.

### `views.py`

Handles HTTP requests, invokes the required processing logic, and returns HTTP/JSON responses.

### `models.py`

Contains module-specific data models when they are actually required. It is not mandatory for every module.

## 7. Documentation

The `docs/` directory contains project-level documentation.

```text
docs/
├── architecture/
└── api/
```

* `architecture/` contains system architecture and structural documentation.
* `api/` contains API-related documentation.

## 8. Root Configuration Files

### `.env.example`

Provides an example template for environment variables and configuration values.

### `.gitignore`

Defines files and directories that should not be committed to version control.

### `docker-compose.yml`

Defines the local/containerized deployment configuration for the independently deployable services.

### `README.md`

Provides the main project documentation and instructions.

## Service Isolation Principle

The most important architectural rule is that the four backend applications remain independent.

```text
                         Frontend
                            │
                            ▼
                           BFF
                            │
              ┌─────────────┼─────────────┐
              │             │             │
             HTTP          HTTP          HTTP
              │             │             │
              ▼             ▼             ▼
       Multilingual +   Sentiment +   Adaptation
       Aspect Service  Stance Service   Service
```

Services communicate through **HTTP APIs**, not through direct Python imports.

There is intentionally no shared:

```text
common/
contracts/
utils/
models/
```

package at the repository level.

This isolation allows each service to have its own dependencies, implementation, configuration, testing, Docker image, and deployment lifecycle.
