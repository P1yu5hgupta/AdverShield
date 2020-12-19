import cv2
import os

data = []
for root, dirs, files in os.walk("."):
    for filename in files:
        data.append(filename)

for image_path in data:
    if image_path.split(".")[-1] == "jpg":
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        print(image_path)
        print('Original Dimensions : ', img.shape)
        scale_percent = 60  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (100, 100)
        # resize image
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        print('Resized Dimensions : ', resized.shape)
        #     cv2.imshow("Resized image", resized)
        cv2.imwrite(image_path, resized)
