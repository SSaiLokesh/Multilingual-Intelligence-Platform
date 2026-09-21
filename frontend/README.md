# Continuous Multilingual Aspect Sentiment and Stance Intelligence Platform

Frontend application for the Continuous Multilingual Aspect Sentiment and Stance Intelligence Platform.

The frontend is implemented using React and Vite and communicates exclusively with the Flask Backend-for-Frontend (BFF).

---

## Architecture

```text
React Frontend
      |
      v
Flask BFF
localhost:8000/api/v1
      |
      +----------------+
      |                |
      v                v
 NLP Services     Adaptation
````

The frontend does not directly communicate with internal backend services.

---

## Technology

* React
* Vite
* JavaScript
* React Router
* CSS
* Fetch API

---

## Project Structure

```text
src/
├── app/
├── pages/
├── components/
├── services/
├── utils/
└── styles/
```

---

## Environment

Create a `.env` file in the project root:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

## Installation

Install dependencies:

```bash
npm install
```

---

## Development

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## Backend

The frontend communicates with:

```text
http://localhost:8000/api/v1
```

The primary MVP endpoint is:

```text
POST /api/v1/process/text
```

Therefore the complete endpoint is:

```text
http://localhost:8000/api/v1/process/text
```

---

## Frontend Routes

| Route       | Page      |
| ----------- | --------- |
| `/`         | Dashboard |
| `/analyze`  | Analyze   |
| `/memory`   | Memory    |
| `/versions` | Versions  |

---

## API Architecture

```text
Page
 |
 v
Domain Service
 |
 v
api.js
 |
 v
Flask BFF
```

React components must not directly call internal ML services.

---

## Internal Services

The following services are internal backend services and must not be called directly by the frontend:

```text
localhost:8001
localhost:8002
localhost:8003
```

Only the BFF is exposed to the frontend.

---

## MVP Analysis Flow

```text
User enters text
      |
      v
Text validation
      |
      v
analysisService
      |
      v
api.js
      |
      v
POST /api/v1/process/text
      |
      v
Flask BFF
      |
      v
Analysis result
      |
      v
Frontend result display
```

---

## Main Analysis Outputs

The frontend displays:

* Detected language
* Language confidence
* Aspect
* Aspect category
* Sentiment
* Sentiment confidence
* Stance target
* Stance
* Stance confidence
* Adaptation status
* Request ID

---

## Future Extensions

The frontend architecture can later support:

* XLM-R
* ABSA
* Stance Detection
* Confidence Evaluation
* Pseudo-labeling
* Replay Buffer
* LoRA Adaptation
* Model Versioning
* Dataset Processing

````

---

# 24. Your Complete Frontend Now

After pasting all of the above, your project should look like this:

```text
frontend/
│
├── public/
│   └── favicon.svg
│
├── src/
│   │
│   ├── app/
│   │   ├── App.jsx
│   │   └── routes.jsx
│   │
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── Analyze.jsx
│   │   ├── Memory.jsx
│   │   └── Versions.jsx
│   │
│   ├── components/
│   │   ├── Layout.jsx
│   │   ├── TextInput.jsx
│   │   ├── AnalysisPipeline.jsx
│   │   ├── ResultCard.jsx
│   │   └── StatusMessage.jsx
│   │
│   ├── services/
│   │   ├── api.js
│   │   ├── analysisService.js
│   │   ├── memoryService.js
│   │   └── versionService.js
│   │
│   ├── utils/
│   │   ├── formatters.js
│   │   └── validators.js
│   │
│   ├── styles/
│   │   ├── variables.css
│   │   └── global.css
│   │
│   └── main.jsx
│
├── .env
├── .env.example
├── .gitignore
├── index.html
├── package.json
└── README.md
````

---

# 25. Now Run It

From your `frontend` folder:

```bash
npm install
```

Then:

```bash
npm run dev
```

You should get something like:

```text
VITE v7.x.x  ready

➜  Local:   http://localhost:5173/
```

Open:

```text
http://localhost:5173
```

### Test these four routes:

```text
http://localhost:5173/
```

Dashboard

```text
http://localhost:5173/analyze
```

Analyze

```text
http://localhost:5173/memory
```

Memory

```text
http://localhost:5173/versions
```

Versions

---

# 26. One Important Thing Before Testing Analyze

The **Dashboard and navigation can work without the backend**.

But when you press:

```text
Analyze Text
```

the frontend will try to call:

```text
POST http://localhost:8000/api/v1/process/text
```

So if your Flask BFF is **not running yet**, you will correctly receive a message similar to:

```text
Unable to connect to the analysis service.
Please make sure the Flask BFF is running.
```

That is **not a frontend bug**. It means our frontend has successfully reached the point where it is trying to communicate with the backend.

The architecture is therefore:

```text
                    FRONTEND
                       │
                       │
              analysisService.js
                       │
                       ▼
                    api.js
                       │
                       │ POST
                       ▼
             localhost:8000/api/v1
                       │
                       ▼
                    Flask BFF
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
           8001      8002      8003
```
