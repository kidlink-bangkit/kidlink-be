# Google Cloud Storage configuration
bucket_name = "your-bucket-name"
model_blob_name = "your-model-file-name.h5"
download_destination = "model.h5"  # Destination file name for downloaded model

# Initialize GCS client
storage_client = storage.Client()

# Download the model from GCS during app startup
@app.on_event("startup")
async def download_model():
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(model_blob_name)
        blob.download_to_filename(download_destination)
        print("Model downloaded successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download model: {str(e)}")
