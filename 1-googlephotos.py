import os
import json
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pathlib import Path
from dotenv import dotenv_values

config = dotenv_values(".env")

SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly"]
TOKEN_FILE = config["TOKEN_FILE"]
ALBUM_NAME = config["ALBUM_NAME"]
googlePhotosCredsPath = config["googlePhotosKey"]
albumPath = config["albumPath"]
metadata_file_path = config["metadataFilePath"]


# Authenticate and create API client
def get_photos_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(googlePhotosCredsPath, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return build("photoslibrary", "v1", credentials=creds, static_discovery=False)


# Get album ID by name
def get_album_id(service, album_name):
    response = service.albums().list().execute()
    for album in response.get("albums", []):
        if album["title"] == album_name:
            return album["id"]
    return None


# Get media items from album
def get_media_items(service, album_id):
    url = "https://photoslibrary.googleapis.com/v1/mediaItems:search"
    headers = {"Authorization": f"Bearer {service._http.credentials.token}"}
    data = json.dumps({"albumId": album_id})

    response = requests.post(url, headers=headers, data=data).json()
    return response.get("mediaItems", [])


# Download media and metadata
def download_album(service, album_name):
    album_id = get_album_id(service, album_name)
    if not album_id:
        print(f"Album '{album_name}' not found.")
        return

    media_items = get_media_items(service, album_id)

    # Create a new directory for the album
    album_dir = Path(albumPath[:-1])
    album_dir.mkdir(parents=True, exist_ok=True)

    metadata = []
    for item in media_items:
        print(item["mediaMetadata"].keys())
        file_url = item["baseUrl"]
        filename = album_dir / item["filename"]  # Store in the new directory

        # Download the photo
        img_data = requests.get(file_url).content
        with open(filename, "wb") as f:
            f.write(img_data)

        # Save metadata
        metadata.append(
            {
                "filename": item["filename"],
                "creationTime": item["mediaMetadata"]["creationTime"],
                # "location": item["mediaMetadata"].get("location", "N/A"),
            }
        )

    metadata.sort(key=lambda x: x["creationTime"])

    # Save metadata to JSON

    with open(metadata_file_path, "w") as meta_file:
        json.dump(metadata, meta_file, indent=4)

    print(f"Album '{album_name}' downloaded to '{album_dir}' with metadata.")


if __name__ == "__main__":
    service = get_photos_service()
    download_album(service, ALBUM_NAME)
