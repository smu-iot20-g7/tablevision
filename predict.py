from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='1cfca7acab65470db7585605e611ab5b')

# Change the directory to your own directory
model = app.models.get('table_tray')


# predicting
filename = "C:/Users/ss47n/Desktop/model_training/p1.jpg"
img = ClImage(filename=filename)
response = model.predict([img])

concepts = response['outputs'][0]['data']['concepts']

print(concepts[0]['name'])
print(concepts[0]['value'])
print(concepts[1]['name'])
print(concepts[1]['value'])
print()
print('first value, larger than second value?')
print(concepts[0]['value'] > concepts[1]['value'] )