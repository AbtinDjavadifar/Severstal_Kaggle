
import numpy as np
import imageio
from pathlib import Path

image_path = Path('C:/Users/Abtin/Desktop/Steel/output_binary/012f26693.png')

# np.set_printoptions(threshold=sys.maxsize)

im = np.array(imageio.imread(image_path))
print(np.unique(im))