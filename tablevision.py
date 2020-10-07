import sys, time, os
from datetime import datetime
import cv2
from clarifai.rest import ClarifaiApp, Image as ClImage

# ======================================
# API KEYS
# ======================================
CLARIFAI_SECRET = os.environ["CLARIFAI_SECRET"]


# ======================================
# Code begins
# ======================================

try:
    video_capture = cv2.VideoCapture("http://" + os.environ["PI_IPV4"] + ":9090/stream/video.mjpeg")
except:
    sys.exit()

app = ClarifaiApp(api_key=CLARIFAI_SECRET)

# Clarifai training model version
model = app.public_models.general_model
model_version = 'aa7f35c01e0642fda5cf400f543e7c40'

success,image = video_capture.read()

# check if video is working;
# vid_capture is a boolean if any 
# video frames can be read
vid_capture, frame = video_capture.read()

while(vid_capture):
    # Capture frame-by-frame
    vid_capture, frame = video_capture.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
video_capture.release()
cv2.destroyAllWindows()