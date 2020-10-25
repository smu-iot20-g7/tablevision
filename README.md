# Tablevision

Monitor table occupancy status at Beo Crescent Hawker Centre based on crockeries/receptacles left on tables and patron occupancy.

## APIs used

**_Tablevision v1 [deprecated]_**: [Clarifai](https://www.clarifai.com)

**_Tablevision v2_**: [Google Cloud AutoML Vision](https://cloud.google.com/vision/automl/docs/tutorial)

## Tablevision device environments

> There are three environments to run Tablevision:
> 
> **"IoT"**: Raspberry Pi
> 
> **"Initialiser"**: Device with GUI (laptop or Pi connected to screen)
> 
> **"Processer"**: Logic-processing endpoint

-------

- **Raspberry Pi – `_sender`**: _To capture the image from the Raspberry Pi's main camera and send it to our API endpoint, `tablevision_processer`._

- **Local device (Our macOS) – `_initialiser`**: _To map out each table from an image using a GUI. Can be run on Raspberry Pi as well, if a GUI is enabled and a screen is connected on the Pi._

- **API Endpoint on the Cloud (Our EC2) – `_processer`**: _Endpoint for Raspberry Pi to send image to and processes each frame and sends it to the Google Cloud AutoML API with our custom Tablevision model. Receives the object prediction results and processes the logic by updating our NoSQL database._

## Instructions

1. Check that the EC2 instance is running
2. On the Pi, capture a still image using `raspistill -o initialise.jpg`
3. Transfer `initialise.jpg` to your local device. **_Skip this step if Pi is connected to a monitor and GUI is enabled._**
4. In the `tablevision_initialiser` folder, specify your image name in the `imagecrop.py` file.
5. Get coordinates of tables using `imagecrop.py`.
6. In the same folder, run `initialise.py` and use the parameters provided by `imagecrop.py` in the sysargs. See example below.
7. Ensure `tablevision_sender/tablevision.py` is running on the Raspberry Pi.

_Step 6 example:_

```
python3 initialise.py '{"46": [[0.03948170731707307, 0.09692911255411243], [0.4337906504065041, 0.09692911255411243], [0.03948170731707307, 0.4648944805194804], [0.4337906504065041, 0.4648944805194804]]}'
```