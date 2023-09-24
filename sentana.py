# importing the required libraries
import requests
import json
import time
import pandas as pd

api_key = "186314e463ab4e3d9ce69fd7a143038b"

# uploading the audio file to assemblyai api, using a post method
audio_file = "datasets\call_111.mp3"
# setting up api endpoints and header
base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization": api_key
}

# uploading audio file to assemblyai api
with open(audio_file, "rb") as f:
  response = requests.post(base_url + "/upload",headers=headers,data=f)

print(response.content)
upload_url = response.json()["upload_url"]

data = {
    "audio_url": upload_url 
}

# making the post request
url = base_url + "/transcript"
response = requests.post(url, json=data, headers=headers)

# extracting the transcript id from the json response body
transcript_id = response.json()['id']
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

# loop around until id is available i.e status is completed
while True:
  transcription_result = requests.get(polling_endpoint, headers=headers).json()

  if transcription_result['status'] == 'completed':
    print(transcription_result['text'])
    break

  elif transcription_result['status'] == 'error':
    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

  else:
    time.sleep(3)