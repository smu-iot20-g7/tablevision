import os, sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from mongoengine import connect
import base64
from google.cloud import vision
from table import Table
import json
import traceback

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

# initialise once pi has started
TABLES = {}

app = Flask(__name__)
CORS(app)

@app.route('/initialise', methods=['POST'])
def initialise():
    # to be able to access the TABLES variable and add objects in
    global TABLES

    data = request.get_json()
    tables_json = json.loads(data['tables_json'])

    try:
        for table_number in tables_json:
            table_object = tables_json[table_number]
            table_number = int(table_number)
            TABLES[table_number] = Table(table_id=table_number, coords=table_object)

        print(TABLES)
        return "table successfully set up", 200
    except:
        traceback.print_exc() 
        return "unexpected error has occured", 400



@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    image64 = data['image64']

    # decode the image back to image
    image_data =  base64.b64decode(image64)
    filename = "test.jpg"
    with open(filename, 'wb') as f:
        f.write(image_data) # save it to test.jpg

    
    # call the cloud vision and get response
    objects = make_request_to_vision(filename)

    # process the objects and update if got people or crockeries
    location_of_objects = process_and_update(objects)

    # update table state liao
    updateTable(location_of_objects)

    return "", 200

def make_request_to_vision(filename):
    client = vision.ImageAnnotatorClient()
    
    with open(filename, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # return objects
    return client.object_localization(image=image).localized_object_annotations


def process_and_update(objects):
    location_of_objects = {
        "people": [], 
        "crockeries": []
    }

    for object in objects:
        formatted_object = resultFormatter(object)

        # boolean and table number
        item_within_table, table_number = itemWithinTable(formatted_object)

        # basically means if there is object within the table, then i shall update
        # either people or crockeries
        if item_within_table:
            if hasPeople(formatted_object):
                if table_number not in location_of_objects["people"]:
                    # means this prediction predicted succesfully a people within that table
                    location_of_objects["people"].append(table_number)

            if hasCrockeries(formatted_object):
                if table_number not in location_of_objects["crockeries"]:
                    location_of_objects["crockeries"].append(table_number)

    return location_of_objects

def resultFormatter(object):
    locations = object.bounding_poly.normalized_vertices
    x = []
    y = []
    
    for key in locations:
        if 'x' not in key:
            x.append(0)
        else:
            x.append(key.x)
        if 'y' not in key:
            y.append(0)
        else:
            y.append(key.y)

    centre = {"x": (min(x) + max(x)) / 2, "y": (min(y) + max(y)) / 2}

    return {
        "name": object.name,
        "location_boundary": locations,
        "score": object.score,
        "mid": object.mid,
        "centre_point": centre
    }

def itemWithinTable(formatted_object):
    # not sure if need declare but just declare 
    global TABLES

    centre_x = formatted_object["centre_point"]["x"]
    centre_y = formatted_object["centre_point"]["y"]

    for table_number in TABLES:

        table_object = TABLES[table_number]

        if table_object.within_coordinates(centre_x, centre_y):
            return True, table_number
        
    return False, ""

def updateTable(location_of_objects):
    # not sure if need declare but just declare 
    global TABLES

    for table_number in TABLES:
        if table_number in location_of_objects["people"]:
            # state 2: has people
            TABLES[table_number].did_change_state(2)
            # TABLES[table_number].print_states()
        elif table_number in location_of_objects["crockeries"] and table_number not in location_of_objects["people"]:
            # state 1: has crockeries, no people
            TABLES[table_number].did_change_state(1)
            # TABLES[table_number].print_states()
        else:
            # state 0: nothing
            TABLES[table_number].did_change_state(0)
            # TABLES[table_number].print_states()


# object == prediction
def hasPeople(object):
    if object.name == "Person" and object.score > 0.84:
        return True
    return False

def hasCrockeries(object):
    if object.name in HAWKER_ITEMS_DICTIONARY and object.score > 0.80:
        return True
    return False


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)