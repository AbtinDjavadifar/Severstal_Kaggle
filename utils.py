import imageio
import numpy as np
import pandas as pd
import os
import cv2
from pathlib import Path

def convert_RLE_to_binary_mask(images_path, annotations_path, csv_path):

    def compute_mask(row, shape, clss):
        width, height = shape

        mask = np.zeros(width * height, dtype=np.uint8)
        pixels = np.array(list(map(int, row.encoded_pixels.split())))
        mask_start = pixels[0::2]
        mask_length = pixels[1::2]

        for s, l in zip(mask_start, mask_length):
            mask[s:s + l] = (clss + 1) * 50

        mask = np.flipud(np.rot90(mask.reshape((height, width))))
        return mask

    def show_image(filename, df):
        row_ids = np.where(df["image_id"] == filename)[0]
        if not row_ids.size:
            raise ValueError(f"Cannot find image {filename}")

        combined_image = None
        for i, row_id in enumerate(row_ids):
            row = df.iloc[row_id]

            filename = os.path.join(images_path, row.image_id)
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

    df = pd.read_csv(csv_path)
    df["image_id"] = df["ImageId_ClassId"].apply(lambda val: val.split("_")[0])
    df["class_id"] = df["ImageId_ClassId"].apply(lambda val: val.split("_")[1])
    df = df.rename(columns={"EncodedPixels": "encoded_pixels"})
    df = df[["image_id", "class_id", "encoded_pixels"]]

    with_pixels = df.dropna()

    ids = with_pixels.image_id.unique()
    for id in ids:
        img = show_image(id, df)
        imageio.imwrite('{}.png'.format(os.path.join(annotations_path, id)[:-4]), img.astype(np.uint8))
        print(id)

def find_RGB_values():

    print(np.unique(np.array(imageio.imread(Path('./Steel/output_binary/012f26693.png')))))

def copy_files(images_path, annotations_path, train_images_path, train_annotations_path):
    files = [file for file in os.listdir(annotations_path) if file.endswith(".png")]

    for file in files:
        shutil.copy("{}.jpg".format(os.path.join(images_path, file)[:-4]), train_images_path)
        shutil.copy(os.path.join(annotations_path, file), train_annotations_path)

def train_test_devider(train_images_path, train_annotations_path, test_images_path, test_annotations_path):
    files = [file for file in os.listdir(train_annotations_path) if file.endswith(".png")]

    test = open("test.txt", "w")

    test_amount = round(0.1 * len(files))

    for x in range(test_amount):
        file = random.choice(files)
        files.remove(file)
        shutil.move("{}.jpg".format(os.path.join(train_images_path, file)[:-4]), test_images_path)
        shutil.move(os.path.join(train_annotations_path, file), test_annotations_path)
        test.write(file + "\n")