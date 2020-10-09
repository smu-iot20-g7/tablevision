from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='1cfca7acab65470db7585605e611ab5b')

# Change the directory to your own directory
img1 = ClImage(file_obj=open('C:/Users/ss47n/Desktop/model_training/tray1.jpg', 'rb'),concepts=['tray'])
img2 = ClImage(file_obj=open('C:/Users/ss47n/Desktop/model_training/tray2.jpg', 'rb'),concepts=['tray'])
img3 = ClImage(file_obj=open('C:/Users/ss47n/Desktop/model_training/tray3.jpg', 'rb'),concepts=['tray'])
img4 = ClImage(file_obj=open('C:/Users/ss47n/Desktop/model_training/tray4.jpg', 'rb'),concepts=['tray'])
img5 = ClImage(file_obj=open('C:/Users/ss47n/Desktop/model_training/tray5.jpg', 'rb'),concepts=['tray'])
img6 = ClImage(file_obj=open('C:/Users/ss47n/Desktop/model_training/tray6.jpg', 'rb'),concepts=['tray'])
img7 = ClImage(file_obj=open('C:/Users/ss47n/Desktop/model_training/tray7.jpg', 'rb'),concepts=['tray'])
# img3 = ClImage(file_obj=open('C:/Users/ss47n/Desktop/notray1.jpg', 'rb'),concepts=['no_tray'])


app.inputs.bulk_create_images([img1, img2, img3, img4, img5, img6, img7])

model = app.models.get('table_tray')
model.train()


# predicting
# filename = "C:/Users/ss47n/Desktop/lib2.jpg"
# img = ClImage(filename=filename)
# response = model.predict([img])

# concepts = response['outputs'][0]['data']['concepts']

# print(concepts)