import colorsys
import os
import random

import cv2
from django.conf import settings


def blur_face(image, factor=3.0):
    # automatically determine the size of the blurring kernel based
    # on the spatial dimensions of the input image
    h, w, _ = image.shape
    kW = int(w // factor)
    kH = int(h // factor)
    # ensure the width and height of the kernel are odd
    kW = kW - 1 if kW % 2 == 0 else kW
    kH = kH - 1 if kH % 2 == 0 else kH
    return cv2.GaussianBlur(image, (kW, kH), sigmaX=0)


def blur_image(img_path, img_path_final, faces):
    img = cv2.imread(img_path)
    # img = imutils.resize(img, width=500)
    count = 1
    for (x, y, w, h) in faces:
        print(count)
        region_of_interest = img[y:y + h, x:x + w]
        img[y:y + h, x:x + w] = blur_face(region_of_interest)
        count += 1
    cv2.imwrite(img_path_final, img)


def pixelate_face(image):
    h, w, _ = image.shape
    w_pixel, h_pixel = (w // 7, h // 7)
    # Resize input to "pixelated" size
    temp = cv2.resize(image, dsize=(w_pixel, h_pixel), interpolation=cv2.INTER_NEAREST)
    return cv2.resize(temp, dsize=(w, h), interpolation=cv2.INTER_NEAREST)


def pixelate_image(img_path, img_path_final, faces):
    print("from pixealate")
    print(img_path)
    print(img_path_final)
    img = cv2.imread(img_path)
    for (x, y, w, h) in faces:
        region_of_interest = img[y:y + h, x:x + w]
        img[y:y + h, x:x + w] = pixelate_face(region_of_interest)
    cv2.imwrite(img_path_final, img)


def _get_faces(img):
    face_cascade_path = os.path.join(settings.BASE_DIR, 'obfuscator', 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    print(face_cascade)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(image=gray, scaleFactor=1.4, minNeighbors=5)


def _random_bright_color():
    h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
    r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
    return r, g, b


def number_faces(img_path, img_path_final):
    img = cv2.imread(img_path)
    faces = _get_faces(img)
    count = 0
    for (x, y, w, h) in faces:
        count += 1
        color = _random_bright_color()
        cv2.rectangle(img, (x, y), (x + w, y + h), color=color, thickness=2)
        cv2.putText(img, str(count),
                    (x + (w // 7 * 3), y - 2),
                    fontFace=1,
                    fontScale=2,
                    color=color,
                    thickness=3,
                    lineType=5)

    cv2.imwrite(img_path_final, img)
    faces_str = str(faces.tolist())
    return faces_str, count
    # to recover list of lists from the str:
    # new_faces = ast.literal_eval(faces_str)
