from fastapi import FastAPI, Query
from azure_service import get_metadata_by_interaction_id, get_metadata_by_date, get_audio_file
from fastapi.middleware.cors import CORSMiddleware
import azure.functions as func
import uvicorn
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  python -m uvicorn main:app --host 127.0.0.1 --port 8000

@app.get("/metadata/interaction/{interaction_id}")
async def fetch_metadata_by_interaction(interaction_id: str):
    return get_metadata_by_interaction_id(interaction_id)

@app.get("/metadata/date/")
async def fetch_metadata_by_date(start_date: str = Query(...), end_date: str = Query(...)):
    return get_metadata_by_date(start_date, end_date)

@app.get("/audio/{interaction_id}")
async def fetch_audio(interaction_id: str):
    return get_audio_file(interaction_id)

# Azure Function entry point
def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function entry point for HTTP trigger"""
    path = req.url.split("/")[-1]  # Extract path
    response = app.openapi() if path == "docs" else app.routes

    return func.HttpResponse(json.dumps({"routes": [route.path for route in response]}), mimetype="application/json")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
