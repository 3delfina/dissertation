import cv2
import imutils
import colorsys
import cv2
import imutils
from matplotlib import image
import random
import os
from PIL import Image, ImageFilter  # ImageDraw, ImageFont
# from DeepPrivacy.deep_privacy.cli import anonymize_and_get_faces


def _resize_photo(img_path):
    # 770*552 size is used in past experiments
    img = image.imread(img_path)
    (h, w) = img.shape[:2]
    if w <= 552 or h <= 552:
        return
    if w < h:
        img = imutils.resize(img, width=552)
    else:
        img = imutils.resize(img, height=552)
    image.imsave(img_path, img)


def _get_faces(img):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(image=gray, scaleFactor=1.4, minNeighbors=5)

def pixelate_image(img_path, img_path_final):
    # Replicate Pixelate - Mosaic in Photoshop, cell size 15 square.
    img = Image.open(img_path)
    width, height = img.size
    actual_product = width * height
    product = 552 * 770
    smaller_side = width if width < height else height

    if smaller_side < 552:
        requested_size = (actual_product * 15) // product
    else:
        requested_size = 15

    requested_size = 30
    print(requested_size)


    faces = [[488, 126, 582, 246], [658, 133, 750, 254], [295, 128, 387, 250], [575, 17, 619, 77], [156, 194, 242, 298], [132, 181, 159, 214], [58, 171, 78, 205], [787, 31, 807, 74], [30, 193, 50, 215]]
    for (x, y, w, h) in faces:
        box = (x, y, w, h)
        face = img.crop(box)
        imgSmall = face.resize((requested_size, requested_size), resample=Image.BILINEAR)
        # Scale back up using NEAREST to original size
        result = imgSmall.resize(face.size, Image.NEAREST)
        img.paste(result, box)
    img.save(img_path_final)

# def apply_blur(image, factor=3.0):
# 	# automatically determine the size of the blurring kernel based
# 	# on the spatial dimensions of the input image
#     h, w, _ = image.shape
#     kW = int(w / factor)
#     kH = int(h / factor)
#
#     # ensure the width and height of the kernel are odd
#     kW -= 1 if kW % 2 == 0 else kW
#     kH -= 1 if kH % 2 == 0 else kH
#
#     return cv2.GaussianBlur(image, (kW, kH), sigmaX=0)
#
#
# def pixelate(image):
#     h, w, _ = image.shape
#     w_pixel, h_pixel = (w//5, h//5)
#     # Resize input to "pixelated" size
#     temp = cv2.resize(image, dsize=(w_pixel, h_pixel), interpolation=cv2.INTER_NEAREST)
#     cv2.imshow("img", temp)
#     cv2.waitKey()
#     return cv2.resize(temp, dsize=(w, h), interpolation=cv2.INTER_NEAREST)
#
#
# def _get_faces(img):
#     face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     return face_cascade.detectMultiScale(image=gray, scaleFactor=1.4, minNeighbors=5)


if __name__ == "__main__":

    img = _resize_photo('test.jpg') # ('pexels-nathan-cowley-1300402.jpg')
    pixelate_image('test.jpg', 'test-pixel_30.jpg')
    # img = imutils.resize(img, width=500)
    #
    # faces = _get_faces(img)
    # for (x, y, w, h) in faces:
    #     region_of_interest = img[y:y+h, x:x+w]
    #     # pixelated_roi =  pixelate(region_of_interest)
    #     # img[y:y+h, x:x+w] = pixelated_roi
    #     img[y:y+h, x:x+w] = apply_blur(region_of_interest)
    #     #cv2.rectangle(img, (x, y), (x+w, y+h), color=(255, 0, 0), thickness=2)
    #
    # cv2.imshow("img", img)
    # cv2.waitKey()
