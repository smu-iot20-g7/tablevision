# Tablevision

Monitor table occupancy status at Beo Crescent Hawker Centre based on crockeries/receptacles left on tables and patron occupancy.

## APIs used

**_Tablevision v1_**: Clarif.ai _[deprecated]_

**_Tablevision v2_**: Google Cloud Vision & AutoML

## Instructions

1. Check that the EC2 instance is running
2. Get coordinates of tables using `imagecrop.py`
3. Run `initialise.py` and use the parameters provided by `imagecrop.py` in the sysargs ie. `python3 initialise.py '{"46": [[0.03948170731707307, 0.09692911255411243], [0.4337906504065041, 0.09692911255411243], [0.03948170731707307, 0.4648944805194804], [0.4337906504065041, 0.4648944805194804]]}'`
4. Ensure `tablevision.py` is running on the Raspberry Pi