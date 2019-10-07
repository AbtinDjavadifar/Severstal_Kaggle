import os
import shutil
from pathlib import Path

images_path = Path("C:/Users/Abtin/Desktop/Steel/input/severstal-steel-defect-detection/train_images")
annotations_path = Path("C:/Users/Abtin/Desktop/Steel/output_binary")

outputdir_img = Path("C:/Users/Abtin/Desktop/Steel/Supervisely/train/img")
outputdir_ann = Path("C:/Users/Abtin/Desktop/Steel/Supervisely/train/ann")


files = [file for file in os.listdir(annotations_path) if file.endswith(".png")]

for file in files:

    shutil.copy("{}.jpg".format(os.path.join(images_path, file)[:-4]), outputdir_img)
    shutil.copy(os.path.join(annotations_path, file), outputdir_ann)


