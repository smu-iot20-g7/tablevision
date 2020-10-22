from picamera.array import PiRGBArray
from picamera import PiCamera
import json, base64, requests, os, time, sys, json
from datetime import datetime
from datetime import time as dttime
from io import BytesIO
from table import Table

TABLES = {}
TABLE_NUMBERS = []

LAST_REFRESH = datetime.now()

try:
    tables_json = json.loads(sys.argv[1])

    for table_number in tables_json:
        print(table_number)
        curr_table = Table(table_number, tables_json[table_number])
        TABLES[int(table_number)] = curr_table
        TABLE_NUMBERS.append(int(table_number))
        print(TABLE_NUMBERS)
        print(TABLES[int(table_number)].print_states())
except:
    print("You forgot the table coordinates.")
    exit

HAWKER_ITEMS_DICTIONARY = [
    "Coffee cup",
    "Tableware",
    "Food",
    "Saucer",
    "Cutlery",
    "Tray",
    "Plate",
    "Teapot",
    "Drinks"
]

def hasPeople(prediction):
    if prediction['name'] == "Person" and prediction['score'] > 0.84:
        return True
    return False

def hasCrockeries(prediction):
    if prediction["name"] in HAWKER_ITEMS_DICTIONARY and prediction['score'] > 0.80:
        return True
    return False

def resultFormatter(prediction):
    locations = prediction["boundingPoly"]["normalizedVertices"]
    x = []
    y = []
    for key in locations:
        if 'x' not in key:
            x.append(0)
        else:
            x.append(key["x"])
        if 'y' not in key:
            y.append(0)
        else:
            y.append(key["y"])

    centre = {"x": (min(x) + max(x)) / 2, "y": (min(y) + max(y)) / 2}

    return {
        "name": prediction["name"],
        "location_boundary": locations,
        "score": prediction["score"],
        "mid": prediction["mid"],
        "centre_point": centre
    }

def categoriseObjects(object_annotations):
    location_of_objects = {
        "people": [], 
        "crockeries": []
    }

    for prediction in object_annotations:
        formatted_prediction = resultFormatter(prediction)
        item_within_table, table_number = itemWithinTable(formatted_prediction)
        
        if item_within_table:
            print("AA")
            if hasPeople(formatted_prediction):
                if table_number not in location_of_objects["people"]:
                    location_of_objects["people"].append(table_number)
            
            if hasCrockeries(formatted_prediction):
                if table_number not in location_of_objects["crockeries"]:
                    location_of_objects["crockeries"].append(table_number)

    return location_of_objects

def itemWithinTable(formatted_prediction):
    centre_x = formatted_prediction["centre_point"]["x"]
    centre_y = formatted_prediction["centre_point"]["y"]

    for table_number in TABLES:

        table_object = TABLES[table_number]

        if table_object.within_coordinates(centre_x, centre_y):
            return True, table_number
        
    return False, ""

def updateTable(location_of_objects):
    print("checking of got append table number to LOO")
    print(location_of_objects["people"])
    print("checking of got append table number to LOC")
    print(location_of_objects["crockeries"])

    for table_number in TABLES:
        if table_number in location_of_objects["people"]:
            # state 2: has people
            print("changing to 2")
            the_table = TABLES[table_number].did_change_state(2)
            TABLES[table_number].print_states()
        elif table_number in location_of_objects["crockeries"] and table_number not in location_of_objects["people"]:
            # state 1: has crockeries, no people
            print("changing to 1")
            the_table = TABLES[table_number].did_change_state(1)
            TABLES[table_number].print_states()
        else:
            # state 0: nothing
            print("changing to 0")
            the_table = TABLES[table_number].did_change_state(0)
            TABLES[table_number].print_states()

# Check if within operations
def isWithinOperatingHours(start, end, time_now=None):
    # If check time is not given, default to current UTC time
    time_now = time_now or datetime.now().time()

    if start < end:
        return time_now >= start and time_now <= end
    else: # crosses midnight
        return time_now >= start or time_now <= end

def refreshToken():
    stream = os.popen("gcloud auth application-default print-access-token")
    return stream.read().strip().replace("\n", "")

def checkRefreshToken():
    # Define global variable of GOOGLE_AUTH and LAST_REFRESH
    global GOOGLE_AUTH
    global LAST_REFRESH
    
    now = datetime.now()
    now_minute = now.minute

    # if not within the same minute 
    if (now - LAST_REFRESH).seconds >= 60:
        # try to check if its 30mins or just reach next hr
        # print("pass", (now - LAST_REFRESH).seconds)
        if now_minute == 30 or now_minute == 0:
            # refresh token
            print("refreshing token")
            stream = os.popen("gcloud auth application-default print-access-token")
            GOOGLE_AUTH = refreshToken()
            LAST_REFRESH = now
    
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

    # if not(isWithinOperatingHours(dttime(6, 00), dttime(23, 55))):
    #     time.sleep(1)
    #     # print("not within operation liao")
    #     continue
    
    # Always check if there is a need to refresh token
    checkRefreshToken()

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
            json_response = json.loads(response.text)["responses"][0]
            print(json_response)
            if json_response != {}:
                object_annotations = json.loads(response.text)["responses"][0]["localizedObjectAnnotations"]
                location_of_objects = categoriseObjects(object_annotations)
                print("debugginginsidfnsiofhaioh=======")
                print(location_of_objects)
                try:
                    updateTable(location_of_objects)
                except Exception as e:
                    raise
    except Exception as e:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        print("Some error occurred for Tablevision, error is at " + str(line) + ": " + str(e))