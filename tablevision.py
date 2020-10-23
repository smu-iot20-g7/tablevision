from picamera.array import PiRGBArray
from picamera import PiCamera
import json, base64, requests, os, time, sys, json
from datetime import datetime
from datetime import time as dttime

# Check if within operations
def isWithinOperatingHours(start, end, time_now=None):
    # If check time is not given, default to current UTC time
    time_now = time_now or datetime.now().time()

    if start < end:
        return time_now >= start and time_now <= end
    else: # crosses midnight
        return time_now >= start or time_now <= end

###############################
    # Main Application #
###############################

# Initialise the Raspi camera and create a variable to reference the raw camera capture
camera = PiCamera()
# Allow the camera to warmup after initialising
time.sleep(0.1)
# Process Endpoint
process_endpoint = "http://18.139.111.67:5000/process"
# Headers
headers = {"content-type": "application/json"}
while True:
    if not(isWithinOperatingHours(dttime(6, 00), dttime(20, 00))):
        time.sleep(1)
        # print("not within operation liao")
        continue

    camera.capture("test.jpg")
    image = "test.jpg"
    image_64 = base64.b64encode(open(image, "rb").read()).decode("utf-8")

    data = json.dumps({
        "image64": str(image_64)
        })

    try:
        response = requests.post(process_endpoint, data=data, headers=headers)
    except:
        continue