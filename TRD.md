# Technical Requirements Document (TRD)

## Continuous Multilingual Aspect Sentiment and Stance Intelligence Platform

**Document Version:** 1.0
**Project Type:** Machine Learning / NLP / Full-Stack Application
**Architecture:** Frontend → API/Controller → NLP Services → Adaptation Service → Storage → Results
**Primary Objective:** Develop a multilingual NLP platform capable of processing text/datasets, detecting language, extracting and categorizing aspects, performing sentiment analysis and stance detection, and continuously integrating new data with previously processed data.

---

# 1. Introduction

## 1.1 Purpose

This Technical Requirements Document defines the technical requirements, system components, software requirements, machine-learning requirements, data requirements, APIs, storage, processing workflow, and deployment requirements for the **Continuous Multilingual Aspect Sentiment and Stance Intelligence Platform**.

The system will accept individual text or uploaded datasets and process them through multiple NLP services. The system will generate structured outputs including:

* Detected language
* Language confidence
* Extracted aspects
* Aspect categories
* Sentiment
* Sentiment confidence
* Stance
* Stance confidence
* Processing metadata
* Historical/adapted information

---

# 2. System Objectives

The system shall:

1. Detect the language of multilingual text.
2. Extract relevant aspects from the input text.
3. Categorize the extracted aspects.
4. Perform aspect-level sentiment analysis.
5. Detect the stance expressed toward an aspect/topic.
6. Process both individual text and complete datasets.
7. Support batch processing of large datasets.
8. Integrate newly processed data with previously stored data.
9. Maintain historical processing information.
10. Provide confidence/probability values for ML predictions.
11. Provide APIs for communication between system components.
12. Provide an interactive frontend for uploading, processing, filtering, and viewing results.
13. Support continuous improvement/adaptation of the system using newly available data.

---

# 3. High-Level System Architecture

The system shall consist of the following major components:

```text
                    ┌──────────────────────────┐
                    │        FRONTEND          │
                    │ Text / Dataset Upload    │
                    │ Results / Analytics       │
                    └────────────┬─────────────┘
                                 │
                                 │ REST API
                                 ▼
                    ┌──────────────────────────┐
                    │    API / CONTROLLER      │
                    │                          │
                    │ Input Processing         │
                    │ Request Management       │
                    │ Service Orchestration    │
                    │ Output Processing        │
                    │ Storage Management       │
                    └────────────┬─────────────┘
                                 │
                 ┌───────────────┼────────────────┐
                 │               │                │
                 ▼               ▼                ▼
       ┌────────────────┐ ┌───────────────┐ ┌──────────────────┐
       │ NLP SERVICE 1  │ │ NLP SERVICE 2 │ │ ADAPTATION       │
       │                │ │               │ │ SERVICE 3        │
       │ Language       │ │ Sentiment     │ │ Input Processing │
       │ Detection      │ │ Analysis      │ │ Memory Update    │
       │      ↓         │ │      ↓        │ │      ↓           │
       │ Aspect         │ │ Stance        │ │ New + Previous  │
       │ Extraction     │ │ Detection     │ │ Data Integration │
       │      ↓         │ │               │ │      ↓           │
       │ Categorization │ │               │ │ Model/Data       │
       └────────────────┘ └───────────────┘ └──────────────────┘
                 │               │                │
                 └───────────────┼────────────────┘
                                 ▼
                    ┌──────────────────────────┐
                    │     DATA / STORAGE       │
                    │ Raw Data                 │
                    │ Processed Data           │
                    │ Predictions             │
                    │ Historical Data          │
                    │ Model Metadata           │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │       FRONTEND           │
                    │ Results / Tables         │
                    │ Search / Filters         │
                    │ Analytics / Reports      │
                    └──────────────────────────┘
```

---

# 4. Functional Requirements

## 4.1 Frontend Requirements

The frontend shall provide:

### Input Management

* Text input field.
* Dataset upload functionality.
* Support for CSV datasets.
* Dataset preview before processing.
* Input validation.
* Processing initiation controls.

### Result Display

The frontend shall display:

| Output               | Description                   |
| -------------------- | ----------------------------- |
| Input Text           | Original text                 |
| Language             | Detected language             |
| Language Confidence  | Probability/confidence        |
| Aspect               | Extracted aspect              |
| Category             | Aspect category               |
| Sentiment            | Positive / Negative / Neutral |
| Sentiment Confidence | Sentiment probability         |
| Stance               | Support / Against / Neutral   |
| Stance Confidence    | Stance probability            |
| Processing Status    | Success / Error / Pending     |

### Filtering

The frontend shall support:

* Language filtering.
* Sentiment filtering.
* Stance filtering.
* Aspect filtering.
* Category filtering.
* Confidence-based filtering.
* Text search.

### Visualization

The frontend should provide:

* Language distribution.
* Sentiment distribution.
* Stance distribution.
* Aspect distribution.
* Category distribution.
* Confidence statistics.
* Dataset processing statistics.

---

# 5. API / Controller Requirements

The controller acts as the central orchestration layer.

## 5.1 Controller Responsibilities

The controller shall:

1. Receive requests from the frontend.
2. Validate incoming data.
3. Identify the processing type.
4. Preprocess input.
5. Invoke the appropriate NLP services.
6. Transfer intermediate outputs between services.
7. Collect outputs from all services.
8. Trigger the adaptation service.
9. Store raw and processed results.
10. Return final results to the frontend.
11. Handle errors and service failures.
12. Manage batch-processing requests.

---

# 6. API Requirements

The system shall use REST APIs for communication between:

```text
Frontend ↔ Controller
Controller ↔ NLP Service 1
Controller ↔ NLP Service 2
Controller ↔ Adaptation Service
Services ↔ Storage
```

## Suggested API endpoints

### Input

```text
POST /api/v1/process/text
POST /api/v1/process/dataset
```

### Language Detection

```text
POST /api/v1/language/detect
```

### Aspect Processing

```text
POST /api/v1/aspect/extract
POST /api/v1/aspect/categorize
```

### Sentiment

```text
POST /api/v1/sentiment/analyze
```

### Stance

```text
POST /api/v1/stance/predict
```

### Adaptation

```text
POST /api/v1/adaptation/update
GET  /api/v1/adaptation/status
```

### Results

```text
GET /api/v1/results/{id}
GET /api/v1/results
```

---

# 7. NLP Service 1 — Multilingual Processing

## 7.1 Responsibilities

NLP Service 1 shall perform:

```text
Input Text
     ↓
Text Preprocessing
     ↓
Language Detection
     ↓
Aspect Extraction
     ↓
Aspect Categorization
     ↓
Structured Output
```

## 7.2 Language Detection

The system shall:

* Detect the language of each input text.
* Support the project's defined multilingual language set.
* Generate confidence/probability.
* Handle short text.
* Handle noisy text.
* Identify unknown/unsupported languages.
* Handle multilingual/mixed-language inputs where supported.

### Output

```json
{
  "text": "Example text",
  "language": "English",
  "language_code": "en",
  "confidence": 0.96
}
```

---

# 8. Aspect Extraction Requirements

The aspect extraction component shall identify meaningful entities, features, topics, or attributes discussed in the text.

Example:

```text
Input:
"The camera quality is excellent but battery life is poor."

Output:

Aspect 1:
camera quality

Aspect 2:
battery life
```

The system shall preserve the relationship between:

```text
Text → Aspect → Category
```

---

# 9. Aspect Categorization Requirements

Extracted aspects shall be mapped to predefined or dynamically supported categories.

Example:

```text
camera quality → Camera
battery life   → Battery
delivery time  → Delivery
customer care  → Service
```

The categorization mechanism should support model-based classification and/or rule-based fallback where required.

---

# 10. NLP Service 2 — Sentiment and Stance

NLP Service 2 shall contain at least two major processing models.

```text
              NLP SERVICE 2
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   Sentiment Model       Stance Model
          │                   │
          ▼                   ▼
    Sentiment Output      Stance Output
```

---

## 10.1 Sentiment Analysis

The sentiment model shall analyze the sentiment associated with the input/aspect.

Supported classes may include:

```text
Positive
Negative
Neutral
```

The exact classes shall be defined according to the project's training dataset.

### Example

```text
Text:
"The battery life is terrible."

Aspect:
Battery life

Sentiment:
Negative

Confidence:
0.94
```

---

# 11. Stance Detection

The stance model shall determine the position expressed toward a target/aspect/topic.

Example classes:

```text
Support
Against
Neutral
```

The system shall produce:

```text
Target
Stance
Confidence
```

Example:

```text
Target: Product X

Stance: Support

Confidence: 0.91
```

---

# 12. Adaptation Service — Continuous Integration

The third service shall provide the continuous/adaptive component of the platform.

## 12.1 Responsibilities

The adaptation service shall:

1. Receive newly processed data.
2. Retrieve relevant historical data.
3. Compare current and previous data.
4. Integrate new records.
5. Update system memory/state.
6. Track changes in the dataset.
7. Maintain historical versions.
8. Support future model improvement.
9. Store adaptation metadata.

---

# 13. Adaptation Workflow

```text
New Input
    ↓
Input Processing
    ↓
NLP Predictions
    ↓
Current Processed Data
    ↓
Retrieve Previous Data
    ↓
Compare / Validate
    ↓
Merge New + Previous Data
    ↓
Update Memory / Dataset
    ↓
Store Updated State
```

The adaptation service should **not automatically retrain production models on every request**. Model retraining should be controlled through a defined training/update pipeline.

---

# 14. Data Requirements

## 14.1 Input Data

The system shall support:

* Individual text.
* CSV datasets.
* Structured multilingual datasets.
* Previously processed datasets.
* Newly collected data.

## 14.2 Existing Project Dataset

The current project dataset may contain fields such as:

```text
source_file
text
aspect
category
sentiment
```

For the expanded system, additional fields should be supported:

```text
language
language_confidence
aspect
category
sentiment
sentiment_confidence
stance
stance_confidence
processing_timestamp
model_version
```

---

# 15. Recommended Final Dataset Schema

| Column                 | Type     | Description          |
| ---------------------- | -------- | -------------------- |
| `id`                   | String   | Unique record ID     |
| `source_file`          | String   | Original data source |
| `text`                 | Text     | Input text           |
| `language`             | String   | Detected language    |
| `language_confidence`  | Float    | Language confidence  |
| `aspect`               | String   | Extracted aspect     |
| `category`             | String   | Aspect category      |
| `sentiment`            | String   | Sentiment class      |
| `sentiment_confidence` | Float    | Sentiment confidence |
| `stance`               | String   | Stance class         |
| `stance_confidence`    | Float    | Stance confidence    |
| `model_version`        | String   | Model used           |
| `processed_at`         | DateTime | Processing timestamp |
| `status`               | String   | Processing status    |

---

# 16. Data Processing Pipeline

The complete processing pipeline shall be:

```text
                    INPUT
                      │
                      ▼
              Input Validation
                      │
                      ▼
             Text Preprocessing
                      │
                      ▼
            Language Detection
                      │
                      ▼
             Aspect Extraction
                      │
                      ▼
            Aspect Categorization
                      │
                      ▼
       ┌──────────────┴──────────────┐
       ▼                             ▼
Sentiment Analysis             Stance Detection
       │                             │
       └──────────────┬──────────────┘
                      ▼
              Output Integration
                      │
                      ▼
              Adaptation Service
                      │
                      ▼
              Data Integration
                      │
                      ▼
                  Storage
                      │
                      ▼
              Results / Analytics
```

---

# 17. Machine Learning Requirements

## 17.1 Training Environment

The initial ML training environment shall be:

**Google Colab**

Training should support GPU acceleration where required.

## 17.2 Training Pipeline

```text
Dataset Collection
       ↓
Data Cleaning
       ↓
Data Validation
       ↓
Label Preparation
       ↓
Train / Validation / Test Split
       ↓
Tokenizer / Feature Processing
       ↓
Model Training
       ↓
Validation
       ↓
Hyperparameter Tuning
       ↓
Final Testing
       ↓
Evaluation
       ↓
Model Export
```

---

# 18. Language Detection Model Requirements

The language detection model shall:

* Support the project's selected languages.
* Process individual and batch text.
* Return language labels.
* Return confidence/probability.
* Handle unseen/noisy text as far as practical.
* Be evaluated on held-out multilingual data.
* Be versioned after training.

### Evaluation metrics

* Accuracy
* Precision
* Recall
* F1-score
* Confusion matrix

For imbalanced multilingual data, **macro-F1** should also be reported.

---

# 19. Sentiment Model Requirements

The sentiment model shall:

* Accept processed text and/or aspect-target information.
* Predict the defined sentiment classes.
* Return confidence values.
* Support multilingual input according to the project's supported languages.
* Be evaluated on a separate test set.

Metrics:

```text
Accuracy
Precision
Recall
F1-score
Macro-F1
Confusion Matrix
```

---

# 20. Stance Model Requirements

The stance model shall:

* Accept text and target/aspect.
* Predict the defined stance classes.
* Return confidence.
* Support multilingual data where training data permits.
* Be evaluated independently.

Example:

```text
Input:
Text + Target

Output:
Target
Stance
Confidence
```

---

# 21. Model Management

Every deployed model should have:

```text
Model Name
Model Version
Training Dataset Version
Training Date
Supported Languages
Evaluation Metrics
Configuration
```

Example:

```text
language-model-v1.0
sentiment-model-v1.0
stance-model-v1.0
aspect-model-v1.0
```

---

# 22. Storage Requirements

The storage layer shall maintain:

### Raw Data

Original uploaded datasets/text.

### Processed Data

NLP-generated results.

### Historical Data

Previous processing results and versions.

### Model Metadata

Information about deployed ML models.

### Processing Metadata

```text
timestamp
request_id
model_version
processing_status
error_information
```

---

# 23. Error Handling Requirements

The system shall handle:

* Invalid file formats.
* Empty datasets.
* Empty text.
* Missing columns.
* Unsupported languages.
* ML model failures.
* API failures.
* Storage failures.
* Invalid API requests.
* Large dataset processing errors.

Example:

```json
{
  "status": "error",
  "code": "INVALID_DATASET",
  "message": "Required text column is missing"
}
```

---

# 24. Batch Processing Requirements

For dataset uploads, the system shall:

1. Validate the complete dataset.
2. Identify valid and invalid records.
3. Process records in batches.
4. Track processing progress.
5. Avoid losing already processed records.
6. Store intermediate results when appropriate.
7. Return a final consolidated dataset.

Example:

```text
10,000 rows
     ↓
Batch 1 → 1,000
Batch 2 → 1,000
...
Batch 10 → 1,000
     ↓
Final Consolidated Dataset
```

---

# 25. Security Requirements

The system shall implement:

* API authentication where required.
* Input validation.
* File type validation.
* File size limits.
* Secure API communication.
* Access control for stored datasets.
* Protection against malicious file uploads.
* Secure storage of credentials/API keys.
* No hard-coded secrets in source code.

---

# 26. Performance Requirements

The system should:

* Support both single-text and batch processing.
* Process datasets efficiently.
* Use asynchronous/background processing for large datasets where necessary.
* Avoid unnecessary repeated model loading.
* Cache models in memory where appropriate.
* Provide processing status for long-running requests.

---

# 27. Frontend–Backend Communication

The recommended flow is:

```text
Frontend
   │
   │ POST /process/dataset
   ▼
Controller
   │
   │ Validate
   ▼
NLP Service 1
   │
   │ language + aspects + categories
   ▼
NLP Service 2
   │
   │ sentiment + stance
   ▼
Adaptation Service
   │
   │ updated dataset/state
   ▼
Storage
   │
   │ processed results
   ▼
Controller
   │
   │ JSON response
   ▼
Frontend
```

---

# 28. Non-Functional Requirements

## Scalability

The architecture should allow individual services to be scaled independently.

## Maintainability

Each service should have a clear responsibility and independent code structure.

## Reliability

Failures in one processing stage should be detected and reported rather than silently producing incorrect results.

## Extensibility

The system should allow future addition of:

* New languages.
* New sentiment classes.
* New stance classes.
* New NLP models.
* New aspect categories.
* New adaptation strategies.

## Reproducibility

The system should record model and dataset versions so that results can be reproduced.

---

# 29. Suggested Technology Stack

| Layer            | Recommended Technology              |
| ---------------- | ----------------------------------- |
| Frontend         | React.js                            |
| UI               | HTML / CSS / JavaScript             |
| Backend          | Python FastAPI                      |
| API              | REST                                |
| ML               | Python                              |
| NLP              | Hugging Face Transformers / PyTorch |
| Data Processing  | Pandas / NumPy                      |
| Training         | Google Colab                        |
| Database         | PostgreSQL                          |
| File Storage     | Local/S3-compatible storage         |
| API Testing      | Postman                             |
| Version Control  | Git + GitHub                        |
| Containerization | Docker                              |
| Documentation    | Markdown / Swagger/OpenAPI          |

These are recommended technologies rather than mandatory choices; the team can finalize them according to implementation constraints.

---

# 30. Project Repository Structure

A suitable repository structure is:

```text
project-root/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│
├── backend/
│   ├── api/
│   ├── controllers/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   └── database/
│
├── ml/
│   ├── language_detection/
│   ├── aspect_extraction/
│   ├── aspect_categorization/
│   ├── sentiment/
│   └── stance/
│
├── adaptation/
│   ├── preprocessing/
│   ├── integration/
│   ├── memory/
│   └── versioning/
│
├── datasets/
│   ├── raw/
│   ├── processed/
│   └── evaluation/
│
├── notebooks/
│   └── google_colab/
│
├── models/
│
├── tests/
│
├── docs/
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# 31. End-to-End Workflow

The final system workflow shall be:

```text
USER
 │
 ▼
FRONTEND
 │
 │ Text / Dataset
 ▼
API / CONTROLLER
 │
 ├── Input Processing
 │
 ▼
NLP SERVICE 1
 │
 ├── Language Detection
 ├── Aspect Extraction
 └── Aspect Categorization
 │
 │ Processed NLP Data
 ▼
NLP SERVICE 2
 │
 ├── Sentiment Analysis
 └── Stance Detection
 │
 │ Enriched Results
 ▼
ADAPTATION SERVICE
 │
 ├── Current Data
 ├── Previous Data
 ├── Data Comparison
 ├── Integration
 └── Memory/State Update
 │
 ▼
STORAGE
 │
 ├── Raw Data
 ├── Processed Data
 ├── Historical Data
 └── Model Metadata
 │
 ▼
CONTROLLER
 │
 │ Final Response
 ▼
FRONTEND
 │
 ├── Result Table
 ├── Search / Filters
 ├── Analytics
 └── Reports
```

---

# 32. Key Technical Design Principle

The most important architectural principle for the project should be:

> **The Controller orchestrates the workflow, while each service owns a clearly defined processing responsibility.**

Therefore:

```text
Controller
    │
    ├── Service 1 → Multilingual + Aspect Processing
    │
    ├── Service 2 → Sentiment + Stance Processing
    │
    └── Service 3 → Continuous Adaptation + Data Integration
```

The services communicate through **well-defined APIs and structured JSON data contracts**, while the storage layer maintains raw, processed, historical, and model-related information.

This separation will make the architecture easier to develop, test, maintain, and extend for the later objectives of the project.
