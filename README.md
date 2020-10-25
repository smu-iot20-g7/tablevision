# Tablevision

Monitor table occupancy status at Beo Crescent Hawker Centre based on crockeries/receptacles left on tables and patron occupancy.

## APIs used

**_Tablevision v1_**: Clarif.ai _[deprecated]_ in the `deprecated/v1` branch

**_Tablevision v2_**: Google Cloud Vision & AutoML

## Tablevision device environments

> There are three environments to run 

- `_initialiser`: local device (our macOS): _To map out each table from an image using a GUI. Can be run on Raspberry Pi as well, if a GUI is enabled and a screen is connected on the Pi._

- `_sender`: Raspberry Pi: _To capture the image from the Raspberry Pi's main camera and send it to our API endpoint, `tablevision_processer`._

- `_processer`: API Endpoint on the Cloud (Our EC2): _Endpoint for Raspberry Pi to send image to and processes each frame and sends it to the Google Cloud AutoML API with our custom Tablevision model. Receives the object prediction results and processes the logic by updating our NoSQL database._

## Instructions

1. Check that the EC2 instance is running
2. In the `tablevision_initialiser` folder, Get coordinates of tables using `imagecrop.py`
3. In the same folder, run `initialise.py` and use the parameters provided by `imagecrop.py` in the sysargs ie. `python3 initialise.py '{"46": [[0.03948170731707307, 0.09692911255411243], [0.4337906504065041, 0.09692911255411243], [0.03948170731707307, 0.4648944805194804], [0.4337906504065041, 0.4648944805194804]]}'`
4. Ensure `tablevision_sender/tablevision.py` is running on the Raspberry Pi