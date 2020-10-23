import os, sys
from flask import Flask, request, jsonify, render_template
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

@app.route('/peek')
def peek_image():
    return render_template("index.html", user_image = '/static/image.jpg')

@app.route('/initialise', methods=['POST'])
def initialise():
    # to be able to access the TABLES variable and add objects in

    data = request.get_json()
    tables_json = json.loads(data['tables_json'])

    try:
        for table_number in tables_json:
            table_object = tables_json[table_number]
            table_number = int(table_number)
            TABLES[table_number] = Table(table_number, table_object)
        
        print(TABLES)
        return jsonify({"type": "success", "message": "Tables successfully set up"}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"type": "error", "message": "unexpected error has occured", "debug": str(e)}), 500

@app.route("/tables/coordinate/<int:table_id>", methods=["GET"])
def getTableCoordinates(table_id):
    try:
        return jsonify({"type": "success", "table_requested": str(table_id), "table_coordinates": TABLES[table_id]}), 200
    except Exception as e:
        return jsonify({"type": "error", "debug": str(e)}), 500

@app.route("/tables", methods=["GET"])
def getTables():
    if len(TABLES) == 0:
        return jsonify({"type": "success", "message": "No tables found"}), 200
    try:
        all_tables = {}
        for table in TABLES:
            all_tables[table] = TABLES[table].print_states()
        json_type = {"type": "success"}
        all_tables.update(json_type)
        return jsonify(all_tables), 200
    except Exception as e:
        return jsonify({"type": "error", "debug": str(e)}), 500

@app.route("/tables/<int:table_id>", methods=["DELETE"])
def deleteTables(table_id):
    try:
        del TABLES[table_id]
        return jsonify({"type": "success", "message": "deleted"}), 201
    except Exception as e:
        return jsonify({"type": "error", "debug": str(e)}), 500


@app.route("/tables", methods=["DELETE"])
def deleteAllTables():
    try:
        TABLES = {}
        return jsonify({"type": "success", "message": "deleted all tables"}), 201
    except Exception as e:
        return jsonify({"type": "error", "debug": str(e)}), 500
    

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        image64 = data['image64']

        # decode the image back to image
        image_data =  base64.b64decode(image64)
        filename = "test.jpg"
        with open(filename, 'wb') as f:
            f.write(image_data) # save it to test.jpg

        with open('/home/ubuntu/processer/static/image.jpg', 'wb') as f:
            f.write(image_data) # save it to for rendering to image
        
        # call the cloud vision and get response
        predictions = makeGoogleRequest(filename)

        # process the objects and update if got people or crockeries
        location_of_objects = processPrediction(predictions)

        # update table state liao
        updateTable(location_of_objects)

        return jsonify({"type": "success"}), 200
    except Exception as e:
        return jsonify({"type": "error", "debug": str(e)}), 500

def makeGoogleRequest(filename):
    client = vision.ImageAnnotatorClient()
    
    with open(filename, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # return objects
    return client.object_localization(image=image).localized_object_annotations


def processPrediction(predictions):
    location_of_objects = {
        "people": [], 
        "crockeries": []
    }

    for prediction in predictions:
        formatted_object = resultFormatter(prediction)

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

def resultFormatter(prediction):
    locations = prediction.bounding_poly.normalized_vertices
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
        "name": prediction.name,
        "location_boundary": locations,
        "score": prediction.score,
        "mid": prediction.mid,
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

def hasPeople(prediction):
    if prediction["name"] == "Person" and prediction["score"] > 0.84:
        return True
    return False

def hasCrockeries(prediction):
    if prediction["name"] in HAWKER_ITEMS_DICTIONARY and prediction["score"] > 0.80:
        return True
    return False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)