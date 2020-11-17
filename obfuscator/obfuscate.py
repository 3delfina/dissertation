import cv2
import imutils
from django.conf import settings
import os

def blur_face(image, factor=3.0):
	# automatically determine the size of the blurring kernel based
	# on the spatial dimensions of the input image
    h, w, _ = image.shape
    kW = int(w / factor)
    kH = int(h / factor)

    # ensure the width and height of the kernel are odd
    kW -= 1 if kW % 2 == 0 else kW
    kH -= 1 if kH % 2 == 0 else kH

    return cv2.GaussianBlur(image, (kW, kH), sigmaX=0)

def blur_image(img_path, img_path_final):
    img = cv2.imread(img_path)
    #img = imutils.resize(img, width=500)
    print(img_path)
    faces = _get_faces(img)
    for (x, y, w, h) in faces:
        region_of_interest = img[y:y+h, x:x+w]
        img[y:y+h, x:x+w] = blur_face(region_of_interest)
    cv2.imwrite(img_path_final, img)


def pixelate_face(image):
    h, w, _ = image.shape
    w_pixel, h_pixel = (w//5, h//5)
    # Resize input to "pixelated" size
    temp = cv2.resize(image, dsize=(w_pixel, h_pixel), interpolation=cv2.INTER_NEAREST)
    return cv2.resize(temp, dsize=(w, h), interpolation=cv2.INTER_NEAREST)


def pixelate_image(img_path, img_path_final):
    img = cv2.imread(img_path)
    faces = _get_faces(img)
    for (x, y, w, h) in faces:
        region_of_interest = img[y:y+h, x:x+w]
        img[y:y+h, x:x+w] = pixelate_face(region_of_interest)
    cv2.imwrite(img_path_final, img)


def _get_faces(img):
    face_cascade_path = os.path.join(settings.BASE_DIR, 'obfuscator', 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    print(face_cascade)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(image=gray, scaleFactor=1.4, minNeighbors=5)
