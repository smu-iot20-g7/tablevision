# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
#import cv2
import json
import base64
import requests

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)

# grab an image from the camera
#camera.capture(rawCapture, format="bgr")
#image = rawCapture.array
#while True:
camera.capture("test.jpg")
image = "test.jpg"
image_64 = base64.encodestring(open(image, "rb").read())
print(image_64)

r = {
  "requests": [
    {
      "image": {
        "content": image_64
      },
      "features": [
        {
          "maxResults": 10,
          "type": "OBJECT_LOCALIZATION"
        },
      ]
    }
  ]
}

json_request = json.dumps(r)

with open("key.json", "r") as key:
    print()
    gcp_key = "Bearer " + key.read().strip()

headers = {"Authorization": gcp_key, "Content-Type": "application/json; charset=utf-8"}
response = requests.post("https://vision.googleapis.com/v1/images:annotate", headers=headers, data=json_request)

print(response.text)
