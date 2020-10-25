import requests
import base64
import json

# image = "image.jpg"
# image64 = base64.b64encode(open(image, "rb").read()).decode("utf-8")

# data = json.dumps({
#     "image64": str(image64)
# })

# # endpoint = "http://localhost:5000/process"
# endpoint = "http://18.139.111.67:5000/process"
# headers = {"content-type": "application/json"}
# response = requests.post(endpoint, data=data, headers=headers)

# if response.ok:
#     print(response.text)
#     print(response.status_code)
# else:
#     print(response.status_code)


endpoint = "http://18.139.111.67:5000/initialise"
headers = {"content-type": "application/json"}

table_json = json.dumps({"31": [
                                [0.025254065040650316, 0.3187905844155842], 
                                [0.40533536585365854, 0.3187905844155842], 
                                [0.025254065040650316, 0.7273403679653679], 
                                [0.40533536585365854, 0.7273403679653679]
                               ]
                        })

data = json.dumps({
    "tables_json": table_json
})

response = requests.post(endpoint, data=data, headers=headers)

print(response.status_code)
print(response.text)

