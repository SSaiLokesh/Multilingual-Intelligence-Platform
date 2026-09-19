from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from pydantic import BaseModel
import pandas as pd
import io
import uuid
from model_loader import model_handler

app = FastAPI(title="Multilingual Processing Engine")
JOB_DATABASE = {}

class TextPayload(BaseModel):
    text: str

@app.post("/api/v1/detect-single")
async def detect_single(payload: TextPayload):
    result = model_handler.predict(payload.text)
    return {
        "raw_text": payload.text,
        "detected_language": result["language"],
        "confidence": result["confidence"]
    }

def process_batch(job_id: str, df: pd.DataFrame, text_column: str):
    results = [model_handler.predict(str(val)) for val in df[text_column]]
    df['detected_language'] = [r['language'] for r in results]
    df['confidence'] = [r['confidence'] for r in results]
    JOB_DATABASE[job_id] = df

@app.post("/api/v1/upload-dataset")
async def upload_dataset(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...), 
    text_column: str = "text"
):
    if not file.filename.endswith(('.csv', '.tsv')):
        raise HTTPException(status_code=400, detail="Only CSV/TSV files supported.")
    
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    
    if text_column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Column '{text_column}' not found.")
    
    job_id = str(uuid.uuid4())
    background_tasks.add_task(process_batch, job_id, df, text_column)
    
    return {"job_id": job_id, "total_rows": len(df), "status": "Processing"}

@app.get("/api/v1/results/{job_id}")
async def get_results(job_id: str):
    if job_id not in JOB_DATABASE:
        return {"status": "Processing or Job ID not found."}
    return {"status": "Completed", "data": JOB_DATABASE[job_id].to_dict(orient="records")}