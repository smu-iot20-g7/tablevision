from google.cloud import automl



def resultFormatter(prediction):
    locations = prediction.image_object_detection.bounding_box.normalized_vertices

    formatted_locations = []

    for vertices in locations.__iter__():
        formatted_locations.append({"x": vertices.x, "y": vertices.y})

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
        "name": prediction.display_name,
        "location_boundary": formatted_locations,
        "score": prediction.image_object_detection.score,
        "centre_point": centre
    }

file_path = './model_test.jpg'
project_id = 'iot-grp7-vision'
model_id = 'IOD6111580407411507200'

prediction_client = automl.PredictionServiceClient()

# Get the full path of the model.
model_full_id = automl.AutoMlClient.model_path(
    project_id, "us-central1", model_id
)

# Read the file.
with open(file_path, "rb") as content_file:
    content = content_file.read()

image = automl.Image(image_bytes=content)
payload = automl.ExamplePayload(image=image)

# params is additional domain-specific parameters.
# score_threshold is used to filter the result
# https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#predictrequest
params = {"score_threshold": "0.8"}

request = automl.PredictRequest(
    name=model_full_id,
    payload=payload,
    params=params
)
response = prediction_client.predict(request=request)

print("Prediction results:")
for result in response.payload:
    # print("====")
    print(resultFormatter(result))