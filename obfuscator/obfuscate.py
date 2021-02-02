from django.conf import settings

import colorsys
import cv2
import imutils
from matplotlib import image
import random
import os
from PIL import Image, ImageFilter  # ImageDraw, ImageFont
from DeepPrivacy.deep_privacy.cli import anonymize_and_get_faces


def blur_image(img_path, img_path_final, faces):
    img = Image.open(img_path)
    width, height = img.size
    smaller_side = width if width < height else height
    if smaller_side < 552:
        radius = (smaller_side * 4) // 552
    else:
        radius = 4

    for (x, y, w, h) in faces:
        box = (x, y, w, h)
        ic = img.crop(box)
        ic = ic.filter(ImageFilter.GaussianBlur(radius=radius))
        img.paste(ic, box)
    img.save(img_path_final)
    # image.show()


def pixelate_image(img_path, img_path_final, faces):
    # Replicate Pixelate - Mosaic in Photoshop, cell size 15 square.
    img = Image.open(img_path)
    width, height = img.size
    smaller_side = width if width < height else height
    if smaller_side < 552:
        requested_size = (smaller_side * 15) // 552
    else:
        requested_size = 15

    for (x, y, w, h) in faces:
        box = (x, y, w, h)
        face = img.crop(box)
        imgSmall = face.resize((requested_size, requested_size), resample=Image.BILINEAR)
        # Scale back up using NEAREST to original size
        result = imgSmall.resize(face.size, Image.NEAREST)
        img.paste(result, box)
    img.save(img_path_final)


def deepfake_image(img_path, img_path_final, img_deepfake_all, not_chosen):
    img = Image.open(img_path)
    result = Image.open(img_deepfake_all)
    for face_box in not_chosen:
        face = img.crop(face_box)
        result.paste(face, face_box)
    result.save(img_path_final)


def mask_image(img_path, img_path_final, faces):
    img = cv2.imread(img_path)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (w, h), color=(0, 0, 0), thickness=-1)
    cv2.imwrite(img_path_final, img)


def avatar_image(img_path, img_path_final, faces):
    img = Image.open(img_path)
    emoji_path = os.path.join(settings.BASE_DIR, 'obfuscator', 'static', 'obfuscator', 'emoji.png')
    emoji = Image.open(emoji_path)

    for (x, y, w, h) in faces:
        emoji_resized = emoji.resize((w-x, h-y))
        img.paste(emoji_resized, (x, y, w, h), emoji_resized)
    img.save(img_path_final)


def _random_bright_color():
    h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
    r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
    return r, g, b


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


def number_faces(img_path, img_path_final, faces):
    img = cv2.imread(img_path)
    count = 0
    for (x, y, w, h) in faces:
        count += 1
        color = _random_bright_color()
        cv2.rectangle(img, (x, y), (w, h), color=color, thickness=3)
        fontScale = min(w - x, h - y) / 30
        shiftDown = (h - y) // 3
        cv2.putText(img, str(count),
                    (x + ((w - x) // 9 * 3), y + shiftDown),
                    fontFace=1,
                    fontScale=fontScale,
                    color=color,
                    thickness=4,
                    lineType=cv2.LINE_AA)
        cv2.putText(img, str(count),
                    (x + ((w - x) // 9 * 3), y + shiftDown),
                    fontFace=1,
                    fontScale=fontScale,
                    color=(0, 0, 0),
                    thickness=1,
                    lineType=cv2.LINE_AA)

    cv2.imwrite(img_path_final, img)
    faces_str = str(faces.tolist()) if len(faces) > 0 else "[]"
    return faces_str, count
    # to recover list of lists from the str:
    # new_faces = ast.literal_eval(faces_str)


def deepfake_and_number(img_path, img_path_final, faces_path):
    _resize_photo(img_path)
    faces = anonymize_and_get_faces(img_path, img_path_final)[0]
    faces_str, count = number_faces(img_path, faces_path, faces)
    return faces_str, count
