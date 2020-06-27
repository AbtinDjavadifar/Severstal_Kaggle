from utils import *

images_path = Path("./Steel/input/severstal-steel-defect-detection/train_images")
annotations_path = Path("./Steel/output_binary")
csv_path = Path("./Steel/input/severstal-steel-defect-detection/train.csv")

train_images_path = Path("./Steel/Supervisely/train/img")
train_annotations_path = Path("./Steel/Supervisely/train/ann")

test_images_path = Path("./Steel/Supervisely/test/img")
test_annotations_path = Path("./Steel/Supervisely/test/ann")

if __name__ == "__main__":
    convert_RLE_to_binary_mask(images_path, annotations_path, csv_path)
    find_RGB_values()
    copy_files(images_path, annotations_path, train_images_path, train_annotations_path)
    train_test_devider(train_images_path, train_annotations_path, test_images_path, test_annotations_path)
