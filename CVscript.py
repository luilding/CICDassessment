import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import time

img = cv.imread('empire.jpg')

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

plt.imshow(img_gray, 'gray')

local_region_size = 3
kernel_size = 3
k = 0.04
threshold = 1000.0

img_gray = np.float32(img_gray)

Harris_res_img = cv.cornerHarris(img_gray, local_region_size, kernel_size, k)
plt.imshow(Harris_res_img, 'gray')

threshold = 1000

highlighted_colour = [0,0, 225] #makes highlights red
highlighted_image = img.copy()
highlighted_image[Harris_res_img > threshold] = highlighted_colour

print(f"At a threshold of {threshold}, the number of detected corners is {np.sum(Harris_res_img>threshold)}")
    
plt.imshow(highlighted_image[:,:,::-1]) #RGB -> BGR


threshold = 0.001 * Harris_res_img.max()
highlighted_colour = [0,0, 225] #makes highlights red
highlighted_image = img.copy()
highlighted_image[Harris_res_img > threshold] = highlighted_colour

print(f"At a threshold of {threshold}, the number of detected corners is {np.sum(Harris_res_img>threshold)}")
    
plt.imshow(highlighted_image[:,:,::-1]) #RGB -> BGR

sift = cv.SIFT_create()

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
kp = sift.detect(img_gray, None)

img_gray_kp = img_gray.copy()
img_gray_kp = cv.drawKeypoints(img_gray, kp, img_gray_kp)
plt.imshow(img_gray_kp)
print("Number of detected keypoints: %d" % (len(kp)))

cv.imwrite("SIFT keypoints.png", img_gray_kp)

print("Processing complete. Keeping the container running for 5 minutes...")
time.sleep(600) 
