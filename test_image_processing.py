import pytest
import cv2 as cv
import numpy as np

@pytest.fixture
def sample_image():
    #Load sample image
    img = cv.imread('empire.jpg')
    if img is None:
        pytest.fail("Image loading failed.")
    return img

def test_grayscale_conversion(sample_image):
    #Convert to grayscale
    img_gray = cv.cvtColor(sample_image, cv.COLOR_BGR2GRAY)
    assert img_gray is not None, "Grayscale conversion failed."
    assert len(img_gray.shape) == 2, "Image is not grayscale."

def test_harris_corner_detection(sample_image):
    #Convert to grayscale and apply Harris detection
    img_gray = cv.cvtColor(sample_image, cv.COLOR_BGR2GRAY)
    img_gray = np.float32(img_gray)
    Harris_res_img = cv.cornerHarris(img_gray, 3, 3, 0.04)
    assert Harris_res_img is not None, "Harris corner detection failed."
    threshold = 1000
    corner_count = np.sum(Harris_res_img > threshold)
    assert corner_count > 0, f"No corners detected at threshold {threshold}."
