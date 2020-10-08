import sys, time, os, base64
from datetime import datetime
import cv2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2

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
except:
    sys.exit()

# check if video is working;
# vid_capture is a boolean if any 
# video frames can be read
vid_capture, frame = video_capture.read()

while(vid_capture):
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

    # print("===================")
    # print("Predicted concepts:")
    # print("===================")
    for concept in output.data.concepts:

        if concept.name == "people" and concept.value > 0.95:
            print("%s %.2f" % (concept.name, concept.value)) 
            print("===================")
            print("PEOPLE DETECTED")
            print("===================")
            print("")

    # print("===================")
    print("")

# When everything done, release the capture
video_capture.release()
cv2.destroyAllWindows()