# importing the required libraries
import requests
import json
import time
import pandas as pd

api_key = "7322a7a962fb43deb5eeaee8f34e848f"

# uploading the audio file to assemblyai api, using a post method
audio_file = "datasets\call_111.mp3"
# setting up api endpoints and header
base_url = "https://api.assemblyai.com/v2/"

headers = {
    "authorization": api_key
}

# uploading audio file to assemblyai api
with open(audio_file, "rb") as f:
  response = requests.post(base_url + "/upload",headers=headers,data=f)

upload_url = response.json()["upload_url"]

data = {
    "audio_url": upload_url,
    "sentiment_analysis" : True
}

# making the post request
url = base_url + "/transcript"
response = requests.post(url, json=data, headers=headers)

# extracting the transcript id from the json response body
transcript_id = response.json()['id']
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

# loop around until status is completed is available i.e status is completed
while True:
  transcription_result = requests.get(polling_endpoint, headers=headers).json()

  if transcription_result['status'] == 'completed':
    transcript_file = "transcripts.txt"
    with open(transcript_file,"w") as tf:
      json.dump(transcription_result['text'],tf)
    break

  elif transcription_result['status'] == 'error':
    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

  else:
    time.sleep(3)

# saving the sentiment analysis results in a separate file
sent_res_file_name = "sent_analysis_res.txt"
with open(sent_res_file_name,"w") as f:
  sent_res = transcription_result["sentiment_analysis_results"]
  json.dump(sent_res,f, indent=3)

pos, neg, neut = 0, 0, 0
for each_line_ana_res in sent_res:
  if each_line_ana_res["sentiment"] == "NEUTRAL":
    neut += 1
  elif each_line_ana_res["sentiment"] == "POSITIVE":
    pos += 1
  else:
    neg += 1

print(f"Neutral: {neut}\nPositive: {pos}\nNegative: {neg}")

