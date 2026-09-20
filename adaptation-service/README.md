# Adaptation Service

The Adaptation Service is responsible for integrating newly processed
multilingual NLP results with the existing adaptation state.

It is the third backend service in the Multilingual Intelligence Platform.

## Architecture

```text
BFF
 │
 │ HTTP
 ▼
Adaptation Service
 │
 ├── Data Integration
 ├── Memory
 └── Versioning