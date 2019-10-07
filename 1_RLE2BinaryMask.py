import imageio
import numpy as np
import pandas as pd
import os
import cv2
from pathlib import Path


outputdir = Path("C:/Users/Abtin/Desktop/Steel/output_binary")
train_images = Path("C:/Users/Abtin/Desktop/Steel/input/severstal-steel-defect-detection/train_images")
csv_dir = Path("C:/Users/Abtin/Desktop/Steel/input/severstal-steel-defect-detection/train.csv")

df = pd.read_csv(csv_dir)
df["image_id"] = df["ImageId_ClassId"].apply(lambda val: val.split("_")[0])
df["class_id"] = df["ImageId_ClassId"].apply(lambda val: val.split("_")[1])
df = df.rename(columns={"EncodedPixels": "encoded_pixels"})
df = df[["image_id", "class_id", "encoded_pixels"]]

with_pixels = df.dropna()

def compute_mask(row, shape, clss):
    width, height = shape

    mask = np.zeros(width * height, dtype=np.uint8)
    pixels = np.array(list(map(int, row.encoded_pixels.split())))
    mask_start = pixels[0::2]
    mask_length = pixels[1::2]

    for s, l in zip(mask_start, mask_length):
        mask[s:s + l] = (clss + 1)*50

    mask = np.flipud(np.rot90(mask.reshape((height, width))))
    return mask

def show_image(filename, df):
    row_ids = np.where(df["image_id"] == filename)[0]
    if not row_ids.size:
        raise ValueError(f"Cannot find image {filename}")


    combined_image = None
    for i, row_id in enumerate(row_ids):
        row = df.iloc[row_id]

        filename = os.path.join(train_images, row.image_id)
        assert os.path.isfile(filename)

        data = cv2.imread(filename)

        width, height, _ = data.shape
        if i == 0:
            combined_image = np.zeros((width, height), dtype=np.uint8)

        if not isinstance(row.encoded_pixels, str):
            continue

        mask = compute_mask(row, (width, height), i)

        combined_image = cv2.add(mask, combined_image)

    return combined_image

ids = with_pixels.image_id.unique()
for id in ids:

    img = show_image(id, df)
    imageio.imwrite('{}.png'.format(os.path.join(outputdir, id)[:-4]), img.astype(np.uint8))
    print(id)

