Yes. This should be our **first implementation step**.

Before writing the internals of any microservice, we should define the **service contracts**. The contracts become the agreement between BFF ↔ Service 1 ↔ Service 2 ↔ Service 3.

For the MVP, I recommend using **versioned JSON REST contracts** with Pydantic schemas on the Python side.

# 1. Contract architecture

```text
                         BFF
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
        Service 1     Service 2     Service 3
        Multilingual  Sentiment     Adaptation
        + Aspect      + Stance       + Integration
             │            │            │
             └────────────┼────────────┘
                          ▼
                       Storage
```

The important rule is:

> **A service must only depend on the contract of another service, not on its internal implementation.**

For example, Service 2 should not care whether Service 1 uses XLM-R, spaCy, rules, or some completely different model.

It only receives the agreed JSON.

---

# 2. Contract naming

Let's establish this convention:

```text
/api/v1/...
```

for BFF/public APIs.

For internal microservice APIs:

```text
/internal/v1/...
```

So our first contracts are:

```text
BFF
 ├── POST /api/v1/process/text
 └── POST /api/v1/process/dataset

Service 1
 └── POST /internal/v1/process

Service 2
 └── POST /internal/v1/analyze

Service 3
 └── POST /internal/v1/adapt
```

---

# 3. Common contract

All services should use some common metadata.

### Request ID

Every request should have a unique:

```text
request_id
```

Example:

```json
{
  "request_id": "req_8f31a2"
}
```

This allows us to trace:

```text
BFF
 ↓
Service 1
 ↓
Service 2
 ↓
Service 3
```

for the same request.

### API version

The URL already contains:

```text
/internal/v1/
```

so we don't need to duplicate API version information in every payload.

---

# 4. Service 1 contract

## Service 1 responsibility

```text
Multilingual + Aspect Processing
```

Its contract is:

```text
Input
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

### Endpoint

```http
POST /internal/v1/process
```

---

## Service 1 request

```json
{
  "request_id": "req_8f31a2",
  "text": "The camera quality is excellent but battery life is poor."
}
```

That's deliberately simple.

Service 1 owns preprocessing, so BFF does **not** need to know how preprocessing works.

---

## Service 1 response

```json
{
  "request_id": "req_8f31a2",
  "status": "success",
  "data": {
    "text": "The camera quality is excellent but battery life is poor.",
    "language": {
      "name": "English",
      "code": "en",
      "confidence": 0.98
    },
    "aspects": [
      {
        "text": "camera quality",
        "category": "Camera"
      },
      {
        "text": "battery life",
        "category": "Battery"
      }
    ]
  },
  "metadata": {
    "service": "multilingual-aspect-service",
    "service_version": "1.0.0"
  }
}
```

---

# 5. Why `aspects` is an array

Because one text can contain multiple aspects.

```text
"The camera is excellent but the battery is terrible."
```

can produce:

```json
"aspects": [
  {
    "text": "camera",
    "category": "Camera"
  },
  {
    "text": "battery",
    "category": "Battery"
  }
]
```

This is important for the later sentiment relationship.

We need to maintain:

```text
Text
 ├── Aspect 1
 ├── Aspect 2
 └── Aspect 3
```

rather than flattening everything.

---

# 6. Service 2 contract

Service 2 owns:

```text
Sentiment
+
Stance
```

It should receive the output required to perform those tasks.

### Endpoint

```http
POST /internal/v1/analyze
```

---

# 7. Service 2 request

I recommend that we send the **original text + language + aspect information**.

```json
{
  "request_id": "req_8f31a2",
  "text": "The camera quality is excellent but battery life is poor.",
  "language": {
    "code": "en",
    "confidence": 0.98
  },
  "aspects": [
    {
      "text": "camera quality",
      "category": "Camera"
    },
    {
      "text": "battery life",
      "category": "Battery"
    }
  ]
}
```

Why include the original text?

Because sentiment and stance models need the textual context.

---

# 8. Service 2 response

```json
{
  "request_id": "req_8f31a2",
  "status": "success",
  "predictions": [
    {
      "aspect": "camera quality",
      "category": "Camera",
      "sentiment": {
        "label": "positive",
        "confidence": 0.95
      },
      "stance": {
        "label": "support",
        "confidence": 0.91
      }
    },
    {
      "aspect": "battery life",
      "category": "Battery",
      "sentiment": {
        "label": "negative",
        "confidence": 0.93
      },
      "stance": {
        "label": "against",
        "confidence": 0.87
      }
    }
  ],
  "metadata": {
    "service": "sentiment-stance-service",
    "service_version": "1.0.0"
  }
}
```

---

# 9. Important point about stance

We should **not force the stance to be aspect sentiment**.

Conceptually:

```text
Sentiment
    ↓
How does the author feel about the aspect?

Stance
    ↓
What position does the author take toward the target?
```

Therefore our contract should eventually support a separate `target`.

For MVP-1, because the TRD says stance can be toward an aspect/topic, we can initially allow:

```json
{
  "target": "camera quality"
}
```

or:

```json
{
  "target": "Product X"
}
```

So I recommend slightly improving the contract now.

---

# 10. Better Service 2 prediction contract

Instead of tying stance permanently to `aspect`, use:

```json
{
  "aspect": "camera quality",
  "category": "Camera",
  "sentiment": {
    "label": "positive",
    "confidence": 0.95
  },
  "stance": {
    "target": "camera quality",
    "label": "support",
    "confidence": 0.91
  }
}
```

That gives us flexibility later.

For example:

```text
Text:
"I support Product X because its camera is excellent."
```

We could have:

```text
Aspect → camera
Sentiment → positive

Target → Product X
Stance → support
```

This is much closer to the actual conceptual distinction between ABSA and stance.

---

# 11. Service 3 contract

Service 3 owns:

```text
Adaptation
Data Integration
Historical State
Versioning
```

Endpoint:

```http
POST /internal/v1/adapt
```

It should receive the **complete enriched result**, rather than forcing it to call Service 1 or Service 2 itself.

This keeps Service 3 independent.

---

# 12. Service 3 request

```json
{
  "request_id": "req_8f31a2",
  "data": {
    "text": "The camera quality is excellent but battery life is poor.",
    "language": {
      "code": "en",
      "confidence": 0.98
    },
    "predictions": [
      {
        "aspect": "camera quality",
        "category": "Camera",
        "sentiment": {
          "label": "positive",
          "confidence": 0.95
        },
        "stance": {
          "target": "camera quality",
          "label": "support",
          "confidence": 0.91
        }
      },
      {
        "aspect": "battery life",
        "category": "Battery",
        "sentiment": {
          "label": "negative",
          "confidence": 0.93
        },
        "stance": {
          "target": "battery life",
          "label": "against",
          "confidence": 0.87
        }
      }
    ]
  }
}
```

---

# 13. Service 3 response

For MVP-1:

```json
{
  "request_id": "req_8f31a2",
  "status": "success",
  "adaptation": {
    "action": "stored",
    "record_id": "rec_001",
    "is_new": true
  },
  "metadata": {
    "service": "adaptation-service",
    "service_version": "1.0.0"
  }
}
```

Notice that we're **not claiming model adaptation happened**.

For the first MVP:

```text
Adaptation Service
        ↓
Data integration + historical state
```

Later:

```text
Adaptation Service
        ↓
Pseudo-labeling
        ↓
Replay buffer
        ↓
LoRA
        ↓
Model update
```

---

# 14. BFF contract

Now we define the most important contract:

```text
Frontend ↔ BFF
```

The frontend should see a **single unified API**.

---

## BFF input

```http
POST /api/v1/process/text
```

```json
{
  "text": "The camera quality is excellent but battery life is poor."
}
```

---

# 15. BFF internal workflow

The BFF performs:

```text
Request
   │
   ▼
Generate request_id
   │
   ▼
Service 1
   │
   ▼
Receive language + aspects
   │
   ▼
Service 2
   │
   ▼
Receive sentiment + stance
   │
   ▼
Service 3
   │
   ▼
Receive adaptation status
   │
   ▼
Aggregate everything
```

---

# 16. BFF final response

The frontend receives:

```json
{
  "request_id": "req_8f31a2",
  "status": "success",
  "data": {
    "text": "The camera quality is excellent but battery life is poor.",
    "language": {
      "name": "English",
      "code": "en",
      "confidence": 0.98
    },
    "predictions": [
      {
        "aspect": "camera quality",
        "category": "Camera",
        "sentiment": {
          "label": "positive",
          "confidence": 0.95
        },
        "stance": {
          "target": "camera quality",
          "label": "support",
          "confidence": 0.91
        }
      },
      {
        "aspect": "battery life",
        "category": "Battery",
        "sentiment": {
          "label": "negative",
          "confidence": 0.93
        },
        "stance": {
          "target": "battery life",
          "label": "against",
          "confidence": 0.87
        }
      }
    ]
  },
  "processing": {
    "adaptation_status": "stored"
  }
}
```

The frontend doesn't need to know:

```text
Service 1 exists
Service 2 exists
Service 3 exists
```

It simply receives the final platform result.

---

# 17. Error contract

We should standardize errors across **all services**.

For example:

```json
{
  "request_id": "req_8f31a2",
  "status": "error",
  "error": {
    "code": "INVALID_INPUT",
    "message": "Text cannot be empty"
  },
  "metadata": {
    "service": "multilingual-aspect-service",
    "service_version": "1.0.0"
  }
}
```

Possible error codes:

```text
INVALID_INPUT
INVALID_DATASET
UNSUPPORTED_LANGUAGE
PROCESSING_ERROR
MODEL_ERROR
SERVICE_UNAVAILABLE
STORAGE_ERROR
INTERNAL_ERROR
```

The BFF can translate internal errors into a consistent public API response.

---

# 18. Health contracts

Every microservice should also expose:

```http
GET /internal/v1/health
```

Example:

```json
{
  "status": "healthy",
  "service": "multilingual-aspect-service",
  "version": "1.0.0"
}
```

Then later the BFF can check:

```text
Service 1 ✓
Service 2 ✓
Service 3 ✓
```

before processing.

---

# 19. Contract dependency flow

The final dependency should be:

```text
                   BFF
                    │
                    ▼
             ┌─────────────┐
             │  Contract 1 │
             └──────┬──────┘
                    │
                    ▼
               SERVICE 1
                    │
                    │ Contract 1 output
                    ▼
             ┌─────────────┐
             │  Contract 2 │
             └──────┬──────┘
                    │
                    ▼
               SERVICE 2
                    │
                    │ Enriched result
                    ▼
             ┌─────────────┐
             │  Contract 3 │
             └──────┬──────┘
                    │
                    ▼
               SERVICE 3
```

But importantly, **Service 2 does not directly call Service 1**.

The BFF orchestrates:

```text
BFF → Service 1
BFF → Service 2
BFF → Service 3
```

rather than:

```text
Service 2 → Service 1
Service 3 → Service 2
```

That keeps the BFF as the orchestrator exactly as you described.

---

# 20. Contract models

Since we're using Python/FastAPI, the contracts should eventually be represented as Pydantic models.

Conceptually:

```text
contracts/
│
├── common.py
│
├── service1.py
│
├── service2.py
│
├── service3.py
│
└── bff.py
```

For example:

```python
class LanguageResult(BaseModel):
    name: str
    code: str
    confidence: float
```

```python
class AspectResult(BaseModel):
    text: str
    category: str
```

```python
class SentimentResult(BaseModel):
    label: str
    confidence: float
```

```python
class StanceResult(BaseModel):
    target: str
    label: str
    confidence: float
```

These become the **formal contracts**, rather than relying only on documentation.

---

# 21. One change I recommend before we freeze it

There is one architectural detail worth deciding now:

### Don't make the contract depend on a particular ML model.

For example, don't put:

```json
"model": "xlm-roberta-base"
```

into the core prediction structure.

Instead, model information belongs in metadata:

```json
"metadata": {
  "service": "sentiment-stance-service",
  "service_version": "1.0.0",
  "model_version": "sentiment-v1.0"
}
```

That means we can later replace:

```text
XLM-R
```

with another model without breaking the BFF or frontend contract.

---

# 22. Final contracts we should implement

So I would freeze the MVP contracts as:

```text
┌────────────────────────────────────────────────────────────┐
│                        BFF API                             │
│                                                            │
│ POST /api/v1/process/text                                 │
│ POST /api/v1/process/dataset                              │
│ GET  /api/v1/results/{id}                                 │
└───────────────────────────┬────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                 SERVICE 1 CONTRACT                         │
│                                                            │
│ POST /internal/v1/process                                  │
│                                                            │
│ Input  → text                                              │
│ Output → language + aspects + categories                    │
└───────────────────────────┬────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                 SERVICE 2 CONTRACT                         │
│                                                            │
│ POST /internal/v1/analyze                                  │
│                                                            │
│ Input  → text + language + aspects                         │
│ Output → sentiment + stance                                │
└───────────────────────────┬────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                 SERVICE 3 CONTRACT                         │
│                                                            │
│ POST /internal/v1/adapt                                    │
│                                                            │
│ Input  → complete enriched result                          │
│ Output → integration/adaptation status                     │
└────────────────────────────────────────────────────────────┘
```

And every service additionally has:

```text
GET /internal/v1/health
```

### The most important contract principle

```text
                  FRONTEND
                      │
                      ▼
                     BFF
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      SERVICE 1   SERVICE 2   SERVICE 3
          │           │           │
          └───────────┼───────────┘
                      ▼
                    DATA
```

**BFF owns orchestration.
Service 1 owns multilingual/aspect processing.
Service 2 owns sentiment/stance.
Service 3 owns adaptation/integration.**

That gives us a stable boundary before we write the actual implementations.
