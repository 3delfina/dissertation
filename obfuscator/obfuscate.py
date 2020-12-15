from django.conf import settings

import colorsys
import cv2
import imutils
import os
import random
from PIL import Image, ImageFilter, ImageDraw
import subprocess


def blur_face(image, factor=3.0):
    # automatically determine the size of the blurring kernel based
    # on the spatial dimensions of the input image
    h, w, _ = image.shape
    kW = int(w // factor)
    kH = int(h // factor)
    # ensure the width and height of the kernel are odd
    kW = kW - 1 if kW % 2 == 0 else kW
    kH = kH - 1 if kH % 2 == 0 else kH
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=4))
    return blurred_image # cv2.GaussianBlur(image, (kW, kH), sigmaX=0)


def blur_image(img_path, img_path_final, faces):
    # img = cv2.imread(img_path)
    # # img = imutils.resize(img, width=500)
    # count = 1
    # for (x, y, w, h) in faces:
    #     region_of_interest = img[y:y + h, x:x + w]
    #     img[y:y + h, x:x + w] = blur_face(region_of_interest)
    #     count += 1
    # cv2.imwrite(img_path_final, img)

    image = Image.open(img_path)
    for (x, y, w, h) in faces:
        box = (x, y, x+w, y+h)
        ic = image.crop(box)
        ic = ic.filter(ImageFilter.GaussianBlur(radius=4))
        image.paste(ic, box)
    image.save(img_path_final)
    # image.show()


def pixelate_face(image):
    h, w, _ = image.shape
    w_pixel, h_pixel = (w // 7, h // 7)
    # Resize input to "pixelated" size
    temp = cv2.resize(image, dsize=(w_pixel, h_pixel), interpolation=cv2.INTER_NEAREST)
    return cv2.resize(temp, dsize=(w, h), interpolation=cv2.INTER_NEAREST)


def pixelate_image(img_path, img_path_final, faces):
    # Replicate Pixelate - Mosaic in Photoshop, cell size 15 square.
    image = Image.open(img_path)
    for (x, y, w, h) in faces:
        box = (x, y, x+w, y+h)
        face = image.crop(box)
        imgSmall = face.resize((15,15),resample=Image.BILINEAR)
        # Scale back up using NEAREST to original size
        result = imgSmall.resize(face.size,Image.NEAREST)
        image.paste(result, box)
    image.save(img_path_final)


def deepfake_image(img_path, img_path_final, faces, not_chosen):
    # image = Image.open(img_path)
    # for (x, y, w, h) in faces:
    #     box = (x-50, y-50, x+w+10, y+h+10)
    #     face = image.crop(box)
    #     face.save(img_path_final)
    #     subprocess.run(["python3", "DeepPrivacy/anonymize.py", "-s", img_path_final, "-t", img_path_final])
    #     result = Image.open(img_path_final)
    #     image.paste(result, box)
    # image.save(img_path_final)
    #python3 anonymize.py -s /home/marija/Pictures/Mumm_Marija.jpeg -t /home/marija/Pictures/Mumm_Marija_fake.jpeg
    subprocess.run(["python3", "DeepPrivacy/anonymize.py", "-s", img_path, "-t", img_path_final])
    image = Image.open(img_path)
    result = Image.open(img_path_final)
    for (x, y, w, h) in not_chosen:
        box = (x, y-5, x+w, y+h+5)
        face = image.crop(box)
        # face.save(img_path_final)

        # result = Image.open(img_path_final)
        result.paste(face, box)
    result.save(img_path_final)


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


def _resize_photo(img_path):
    # 770*552 size is used in past experiments
    img = cv2.imread(img_path)
    h, w, _ = img.shape
    print(str(h) + " " + str(w))
    if w <= 552 or h <= 552:
        return
    if w < h:
        img = imutils.resize(img, width=552)
    else:
        img = imutils.resize(img, height=552)
    print(img.shape)
    cv2.imwrite(img_path, img)


def number_faces(img_path, img_path_final):
    _resize_photo(img_path)
    img = cv2.imread(img_path)
    faces = _get_faces(img)
    count = 0
    for (x, y, w, h) in faces:
        count += 1
        color = _random_bright_color()
        cv2.rectangle(img, (x, y), (x + w, y + h), color=color, thickness=3)
        fontScale = min(w, h)/30
        cv2.putText(img, str(count),
                    (x + (w // 9 * 3), y - 5),
                    fontFace=1,
                    fontScale=fontScale,
                    color=color,
                    thickness=4,
                    lineType=cv2.LINE_AA)

    cv2.imwrite(img_path_final, img)
    faces_str = str(faces.tolist())
    return faces_str, count
    # to recover list of lists from the str:
    # new_faces = ast.literal_eval(faces_str)
