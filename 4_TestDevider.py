# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 16:54:39 2019

@author: Abtin
"""

import os
import shutil
import random
from pathlib import Path


images_path = Path("C:/Users/Abtin/Desktop/Steel/Supervisely/train/img")
annotations_path = Path("C:/Users/Abtin/Desktop/Steel/Supervisely/train/ann")

images_test = Path("C:/Users/Abtin/Desktop/Steel/Supervisely/test/img")
annotations_test = Path("C:/Users/Abtin/Desktop/Steel/Supervisely/test/ann")

files = [file for file in os.listdir(annotations_path) if file.endswith(".png")]

test = open("test.txt","w")

test_amount = round(0.1*len(files))

for x in range(test_amount):

    file = random.choice(files)
    files.remove(file)
    shutil.move("{}.jpg".format(os.path.join(images_path, file)[:-4]), images_test)
    shutil.move(os.path.join(annotations_path, file), annotations_test)
    test.write(file + "\n")