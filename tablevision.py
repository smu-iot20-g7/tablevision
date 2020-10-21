from picamera.array import PiRGBArray
from picamera import PiCamera
import json, base64, requests, os, time
from io import BytesIO

HAWKER_ITEMS_DICTIONARY = [
    "Coffee cup",
    "Tableware",
    "Food",
    "Saucer",
    "Cutlery",
    "Tray"
]

def refreshToken():
    stream = os.popen("gcloud auth application-default print-access-token")
    return stream.read().strip().replace("\n", "")

def hasPeople(prediction):
    if prediction['name'] == "Person" and prediction['score'] > 0.84:
        return True
    return False

def hasCrockeries(prediction):
    if prediction["name"] in HAWKER_ITEMS_DICTIONARY and prediction['score'] > 0.80:
        return True
    return False

def resultFormatter(prediction):
    return {
        "name": prediction["name"],
        "location_boundary": prediction["boundingPoly"]["normalizedVertices"],
        "score": prediction["score"],
        "mid": prediction["mid"]
    }

def categoriseObjects(object_annotations):
    location_of_objects = {
        "people": [], 
        "crockeries": []
    }

    states_tracker = {
        "has_people": False,
        "has_crockeries": False
    }
    
    for prediction in object_annotations:
        print(prediction)
        if hasPeople(prediction):
            states_tracker["has_people"] = True
            location_of_objects["people"].append(resultFormatter(prediction))
        
        if hasCrockeries(prediction):
            states_tracker["has_crockeries"] = True
            location_of_objects["crockeries"].append(resultFormatter(prediction))

    return states_tracker, location_of_objects

# Check if within operations
def isWithinOperatingHours(start, end, time_now=None):
    # If check time is not given, default to current UTC time
    time_now = time_now or datetime.now().time()
    print(time_now)

    if start < end:
        return time_now >= start and time_now <= end
    else: # crosses midnight
        return time_now >= start or time_now <= end

###############################
    # Main Application #
###############################

# Fetch Google Authentication Token
GOOGLE_AUTH = refreshToken()

# Initialise the Raspi camera and create a variable to reference the raw camera capture
camera = PiCamera()
# Allow the camera to warmup after initialising
time.sleep(0.1)

while True:

    # if not(isWithinOperatingHours(time(6, 00), time(20, 00))):
    #     time.sleep(1)
    #     continue

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

    # Request headers
    headers = {"Authorization": "Bearer " + GOOGLE_AUTH, "Content-Type": "application/json; charset=utf-8"}

    try:
        response = requests.post("https://vision.googleapis.com/v1/images:annotate", headers=headers, data=json_request)

        object_annotations = []

        if response.status_code == 200:
            object_annotations = json.loads(response.text)["responses"][0]["localizedObjectAnnotations"]
            categoriser = categoriseObjects(object_annotations)

            states = categoriser[0]
            location_of_objects = categoriser[1]

            print("===========")
            print(states)
            print("===========")

            #print(location_of_objects)

    except Exception as e:
        print("Some error occurred for Tablevision, error is: " + str(e))