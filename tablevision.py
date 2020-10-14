import sys, time, os, base64, requests
from datetime import datetime
import cv2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2
from table import Table

# TELEGRAM_KEY = os.environ["TELEGRAM_KEY"]
# TELEGRAM_URL = "https://api.telegram.org/bot" + TELEGRAM_KEY

TABLEVISION_API = os.environ["TABLEVISION_API"]

# ======================================
# Clarifai Setup
# ======================================
CLARIFAI_SECRET = os.environ["CLARIFAI_SECRET"]
channel = ClarifaiChannel.get_json_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (("authorization", "Key " + CLARIFAI_SECRET),)

# training model
# currently set to: general model
MODEL = "aaa03c23b3724a16a56b629203edc62c"

# ======================================
# Code begins
# ======================================

try:
    video_capture = cv2.VideoCapture("http://" + os.environ["PI_IPV4"] + ":9090/stream/video.mjpeg")
    table_15 = Table(15)
except:
    sys.exit()

# check if video is working;
# vid_capture is a boolean if any 
# video frames can be read
vid_capture, frame = video_capture.read()

def hasPeople(people_predictor):
    if people_predictor["no person"] >= people_predictor["people"]:
        return False
    else:
        return True

def hasCrockeries(crockeries_predictor):
    if len(crockeries_predictor) != 0:
        return True
    return False

while (vid_capture):
    # Capture frame-by-frame
    vid_capture, frame = video_capture.read()
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Display the resulting frame in a new window in grayscale
    # cv2.imshow("frame",gray)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    retval, buffer = cv2.imencode('.jpg', frame)
    
    # converts image buffer from memory to bytes
    image_frame = buffer.tobytes()
    

    # use the image_frame to send to
    # Clarifai API using gRPC
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            model_id=MODEL,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image_frame
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here.
    output = post_model_outputs_response.outputs[0]
    prediction_results = output.data.concepts

    people_predictor = {"people": 0.00, "no person": 0.00}
    crockeries_predictor = {}

    for concept in prediction_results:
        if concept.name == "no person" or concept.name == "people":
            print("===================")
            print("%s %.2f" % (concept.name, concept.value))
            print("===================")

            people_predictor[concept.name] = concept.value

        if (concept.name == "food" or concept.name == "tableware" or concept.name == "cutlery") and concept.value > 0.85:
            crockeries_predictor[concept.name] = concept.value

    
    table_has_people = hasPeople(people_predictor)
    table_has_crockeries = hasCrockeries(crockeries_predictor)

    try:
        if table_has_people:
            # State 2
            try:
                # msg = "PEOPLE DETECTED, confidence:" + str(concept.value)
                tablevision_api_response = requests.put(TABLEVISION_API + "/15?state=2")
                table_15.did_change_state(2)
                # response = requests.get(TELEGRAM_URL + msg)
                # print("Telegram response:" + str(response))
            except Exception as e:
                raise
        elif table_has_crockeries and not table_has_people:
            # State 1
            try:
                tablevision_api_response = requests.put(TABLEVISION_API + "/15?state=1")
                table_15.did_change_state(1)
            except Exception as e:
                raise
        else:
            # State 0
            try:
                tablevision_api_response = requests.put(TABLEVISION_API + "/15?state=0")
                table_15.did_change_state(0)
            except Exception as e:
                raise
    except Exception as e:
        print("can't send to api, " + str(e))

# When everything done, release the capture
video_capture.release()
cv2.destroyAllWindows()