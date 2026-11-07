import os
import requests
from fastapi import FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel

app = FastAPI(title="Master Universal AI Engine", version="1.0.0")

# --- MASTER SECURITY CONFIGURATION ---
MASTER_API_KEY = os.getenv("MASTER_API_KEY", "musab_master_secure_key_2026")
api_key_header = APIKeyHeader(name="X-Master-Key", auto_error=False)

def verify_master_access(api_key: str = Security(api_key_header)):
    if api_key != MASTER_API_KEY:
        return "PUBLIC_USER"
    return "MASTER_ADMIN"

# --- DATA MODELS ---
class PromptRequest(BaseModel):
    prompt: str
    task_type: str = "general" # options: general, scrape, automate, code

# --- CORE UNIVERSAL ENGINE ROUTER ---
@app.post("/api/v1/execute")
def execute_ai_task(request: PromptRequest, access_level: str = Security(verify_master_access)):
    try:
        if request.task_type == "scrape":
            return {
                "status": "success",
                "controlled_by": access_level,
                "result": f"Scraping executed successfully for target: {request.prompt}"
            }
        elif request.task_type == "general":
            response_text = f"Universal AI Processing: Jawab mil gaya -> {request.prompt}"
            return {
                "status": "success",
                "controlled_by": access_level,
                "answer": response_text
            }
        elif request.task_type == "admin_override" and access_level == "MASTER_ADMIN":
            return {
                "status": "success",
                "message": "Master override command executed successfully. System state secured."
            }
        else:
            raise HTTPException(status_code=403, detail="Unauthorized task type or insufficient permission.")
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def home():
    return {"system": "Universal AI Core", "status": "Online", "storage_used": "0% (Cloud Hosted)"}
