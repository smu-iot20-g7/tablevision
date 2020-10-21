from picamera.array import PiRGBArray
from picamera import PiCamera
import time, datetime, json, base64, requests, os
from io import BytesIO

def refreshToken():
    stream = os.popen("gcloud auth application-default print-access-token")
    return stream.read().strip().replace("\n", "")

def hasPeople(object_annotations):
    locations = []
    for prediction in object_annotations:
        print(prediction)
        if prediction['name'] == "Person" and prediction['score'] > 0.84:
            locations.append(prediction)

    if len(locations) > 0:
        return True, locations

    return False, []


def hasCrockeries(object_annotations):
    if len(crockeries_predictor) != 0:
        return True
    return False

# Check if within operation
def is_within_operating_hours(start, end, now=None):
    # If check time is not given, default to current UTC time
    now = now or datetime.now().time()
    print(now)

    if start < end:
        return now >= start and now <= end
    else: # crosses midnight
        return now >= start or now <= end

GOOGLE_AUTH = refreshToken()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
# rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)

# grab an image from the camera
# camera.capture(rawCapture, format="bgr")
# image = rawCapture.array
while True:
    camera.capture("test.jpg")
    image = "test.jpg"
    image_64 = base64.b64encode(open(image, "rb").read()).decode("utf-8")

    r = {
    "requests": [
        {
        "image": {
            "content": str(image_64)
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
        gcpk = key.read()
        gcp_key = "Bearer " + gcpk.strip().replace("\n", "")

    headers = {"Authorization": "Bearer " + GOOGLE_AUTH, "Content-Type": "application/json; charset=utf-8"}
    response = requests.post("https://vision.googleapis.com/v1/images:annotate", headers=headers, data=json_request)

    object_annotations = []

    if response.ok:
        object_annotations = json.loads(response.text)["responses"][0]["localizedObjectAnnotations"]
        people_prediction = hasPeople(object_annotations)
        if people_prediction[0]:
            print(object_annotations)
            print("HAS PEOPLE")

