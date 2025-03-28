# videoCreator
videos:
1. https://youtu.be/1rHd5U9Xgv8
2. https://youtu.be/-BPH9h7kCE8

.env file
ALBUM_NAME = "add your album name"
baseResourceDirectory = "Downloaded_Albums"
albumPath = ${baseResourceDirectory}/${ALBUM_NAME}/
metadataFilePath = ${baseResourceDirectory}/${ALBUM_NAME}/metadata.json

elevenLabsApi="add you own api key"

API_KEY = "add your own api key"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

this file is auto created. Just leave this as is
TOKEN_FILE = "token.json"

#apis and services, credentials oauth 2.0 client ids
googlePhotosKey = "googlePhotosKey.json"




1. create service account  
2. create key for service account and get key in json
3. export GOOGLE_APPLICATION_CREDENTIALS="serviceAccountGoogle.json"
4. set up your app or Google Auth Platform add test users or publish the app
5. get credentials in apis and services
6. get the name of your album and add it in ALBUM_NAME
7. run "python3.10 -m venv venv"
8. run "source venv/bin/activate"
9. run "pip install -r requirements.txt"
10. run the python scripts in order