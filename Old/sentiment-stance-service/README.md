# Sentiment + Stance Service

Independent Flask microservice responsible for sentiment analysis and stance detection.

## Responsibilities

- Aspect-level sentiment prediction
- Target-level stance prediction
- Prediction confidence generation
- Combining sentiment and stance predictions

## Does Not Handle

- Text preprocessing
- Language detection
- Aspect extraction
- Aspect categorization
- Data adaptation
- BFF orchestration

## Port

8002

## Main Endpoint

POST /internal/v1/analyze

## Individual Endpoints

POST /internal/v1/sentiment/predict

POST /internal/v1/stance/predict

## Main Request

```json
{
    "request_id": "req_12345678",
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
````

## Main Response

```json
{
    "request_id": "req_12345678",
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



Your service should now look like this:

```text
sentiment-stance-service/
│
├── app.py
├── config.py
│
├── models/
│   └── base_models.py
│
├── modules/
│   │
│   ├── process/
│   │   ├── routes.py
│   │   ├── views.py
│   │   └── processor.py
│   │
│   ├── sentiment/
│   │   ├── routes.py
│   │   ├── views.py
│   │   └── processor.py
│   │
│   └── stance/
│       ├── routes.py
│       ├── views.py
│       └── processor.py
│
├── requirements.txt
└── README.md
````

The internal flow is:

```text
                   Service 2
                       │
                       ▼
              process/views.py
                       │
                       ▼
             process/processor.py
                    /     \
                   /       \
                  ▼         ▼
          sentiment       stance
          processor       processor
               │              │
               ▼              ▼
          sentiment        stance
           result           result
                  \          /
                   \        /
                    ▼      ▼
                   Combined
                  Prediction
                       │
                       ▼
                    BFF
```

---

# 20. Run Service 2 independently

Open a terminal inside:

```text
sentiment-stance-service/
```

Create the environment:

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

Install:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
python app.py
```

It should start on:

```text
http://localhost:8002
```

First test:

```text
GET http://localhost:8002/health
```

Expected:

```json
{
    "service": "sentiment-stance-service",
    "status": "healthy"
}
```

Then test the endpoint:

```text
POST http://localhost:8002/internal/v1/analyze
```

with:

```json
{
    "request_id": "req_test_001",
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

You should receive a response containing:

```text
camera quality
    → sentiment
    → stance

battery life
    → sentiment
    → stance
```

### One architectural point to preserve

Even though the current MVP uses simple keyword rules, **sentiment and stance remain two independent modules**:

```text
                    Text + Aspect/Target
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
             Sentiment              Stance
                 │                     │
                 ▼                     ▼
          Positive/Negative/     Support/Against/
             Neutral                Neutral
```

That separation is important because later we can replace `sentiment/processor.py` with the actual **XLM-R-based ABSA model** and `stance/processor.py` with the actual **stance model**, without changing the Service 2 API or the BFF.
