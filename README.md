# Severstal Steel Defect Detection Challenge

This code converts the Severstal dataset to an appropriate input format for using Supervisely for training the convolutional neural networks.

## Running the code
`python main.py`

### An example for setting the classes mapping section on Supervisely
```
{
  "classes_mapping": {
    "type1": 50,
    "type2": 100,
    "type3": 150,
    "type4": 200
  }
}
```