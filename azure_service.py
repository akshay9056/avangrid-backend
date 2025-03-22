import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from fastapi import Response

# Load environment variables
load_dotenv()

AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_STORAGE_ACCOUNT_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER")

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient(
    f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=AZURE_STORAGE_ACCOUNT_KEY
)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

def get_metadata_by_interaction_id(interaction_id: str):
    """
    Fetch metadata of blobs where the name starts with the given interaction_id.
    """
    print(interaction_id)
    blobs = container_client.list_blobs(include=["metadata"],name_starts_with=interaction_id)
    
    metadata_list = []
    
    for blob in blobs:
        metadata = blob.metadata
        print(metadata)
        metadata_list.append(metadata)

    return {"metadata": metadata_list}

def get_metadata_by_date(start_date: str, end_date: str):
    """
    Fetch metadata of blobs where Start_Time falls between start_date and end_date.
    """
    query = f'"Start_time" >= \'{start_date}\' AND "Start_time" <= \'{end_date}\''
    # query = f'"Start_Time" = \'{start_date}\''
    print(query)

    blobs = container_client.find_blobs_by_tags(query)

    metadata_list = []
    for blob in blobs:
        blob_client = container_client.get_blob_client(blob.name)  # Get Blob Client
        blob_properties = blob_client.get_blob_properties()  # Fetch Blob Properties
        metadata = blob_properties.metadata  # Extract Metadata
        if metadata:
            metadata_list.append( metadata)
            print(f"Blob Name: {blob.name}, Metadata: {metadata}")  # Print metadata


    return {"metadata": metadata_list}

def get_audio_file(interaction_id: str):
    """
    Fetch the audio file (MP3) where the filename is {interaction_id}.mp3.
    """
    blob_name = f"{interaction_id}.mp3"
    blob_client = container_client.get_blob_client(blob_name)

    if not blob_client.exists():
        return {"error": "Audio file not found"}

   
    stream = blob_client.download_blob().content_as_bytes()

    return Response(content=stream, media_type="audio/mpeg")
