from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import threading

app = FastAPI()

STATUS_NOT_SERVING = "NOT_SERVING"
STATUS_PENDING = "PENDING"
STATUS_STARTED = "STARTED"
STATUS_RUNNING = "RUNNING"

model_status = {}
loaded_models = {}

class DeployRequest(BaseModel):
    model_name: str

def load_model(model_name):
    try:
        model_status[model_name] = STATUS_STARTED
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        loaded_models[model_name] = pipeline("text-classification", model=model, tokenizer=tokenizer)
        model_status[model_name] = STATUS_RUNNING
    except Exception as e:
        model_status[model_name] = STATUS_NOT_SERVING
        print(f"Failed to load {model_name}: {e}")

@app.post("/deploy")
async def deploy_model(req: DeployRequest):
    model_name = req.model_name
    if model_status.get(model_name) == STATUS_RUNNING:
        return {"message": f"{model_name} is already running"}

    model_status[model_name] = STATUS_PENDING
    threading.Thread(target=load_model, args=(model_name,)).start()
    return {"message": f"Started deploying {model_name}", "status": model_status[model_name]}

@app.get("/status/{model_name}")
async def get_status(model_name: str):
    return {"model_name": model_name, "status": model_status.get(model_name, STATUS_NOT_SERVING)}

@app.post("/predict")
async def predict(request: Request):
    body = await request.json()
    model_name = body.get("model_name")
    text = body.get("text")

    if model_status.get(model_name) != STATUS_RUNNING:
        raise HTTPException(status_code=400, detail="Model is not running")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    return {"result": loaded_models[model_name](text)}
