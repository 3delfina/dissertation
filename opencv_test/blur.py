# import the necessary packages
import numpy as np
import cv2
import imutils

def anonymize_face_simple(image, factor=3.0):
	# automatically determine the size of the blurring kernel based
	# on the spatial dimensions of the input image
	(h, w) = image.shape[:2]
	kW = int(w / factor)
	kH = int(h / factor)
	# ensure the width of the kernel is odd
	if kW % 2 == 0:
		kW -= 1
	# ensure the height of the kernel is odd
	if kH % 2 == 0:
		kH -= 1
	# apply a Gaussian blur to the input image using our computed
	# kernel size
	return cv2.GaussianBlur(image, (kW, kH), 0)

img = cv2.imread('pexels-nathan-cowley-1300402.jpg')
img = imutils.resize(img, width=800)
img = anonymize_face_simple(img, factor=10)
cv2.imshow("img", img)
cv2.waitKey()
