from fastapi import FastAPI, Query
from azure_service import get_metadata_by_interaction_id, get_metadata_by_date, get_audio_file
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/metadata/interaction/{interaction_id}")
async def fetch_metadata_by_interaction(interaction_id: str):
    return get_metadata_by_interaction_id(interaction_id)

@app.get("/metadata/date/")
async def fetch_metadata_by_date(start_date: str = Query(...), end_date: str = Query(...)):
    return get_metadata_by_date(start_date, end_date)

@app.get("/audio/{interaction_id}")
async def fetch_audio(interaction_id: str):
    return get_audio_file(interaction_id)

