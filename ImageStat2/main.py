import cv2
import glob

for img in glob.glob("path/to/folder/*.png"):
    cv_img = cv2.imread(img)
