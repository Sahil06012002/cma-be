import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from fastapi import UploadFile, HTTPException
from typing import List

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "product-images"

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

container_client = blob_service_client.get_container_client(CONTAINER_NAME)


async def upload_images_to_blob(photos: List[UploadFile]) -> List[str]:
    image_urls = []

    for photo in photos:
        try:
            blob_name = f"{photo.filename}"
            blob_client = container_client.get_blob_client(blob_name)

            with photo.file as f:
                blob_client.upload_blob(f, overwrite=True)

            image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
            image_urls.append(image_url)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")
    
    return image_urls
