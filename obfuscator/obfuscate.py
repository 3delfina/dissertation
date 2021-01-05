from django.conf import settings

import colorsys
import imutils
import os
from matplotlib import image
import random
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from DeepPrivacy.deep_privacy.cli import anonymize_and_get_faces


def blur_image(img_path, img_path_final, faces):
    image = Image.open(img_path)
    for (x, y, w, h) in faces:
        box = (x, y, w, h)
        ic = image.crop(box)
        ic = ic.filter(ImageFilter.GaussianBlur(radius=4))
        image.paste(ic, box)
    image.save(img_path_final)
    # image.show()


def pixelate_image(img_path, img_path_final, faces):
    # Replicate Pixelate - Mosaic in Photoshop, cell size 15 square.
    image = Image.open(img_path)
    for (x, y, w, h) in faces:
        box = (x, y, w, h)
        face = image.crop(box)
        imgSmall = face.resize((15, 15), resample=Image.BILINEAR)
        # Scale back up using NEAREST to original size
        result = imgSmall.resize(face.size, Image.NEAREST)
        image.paste(result, box)
    image.save(img_path_final)


def deepfake_image(img_path, img_path_final, img_deepfake_all, not_chosen):
    image = Image.open(img_path)
    result = Image.open(img_deepfake_all)
    for face_box in not_chosen:
        face = image.crop(face_box)
        result.paste(face, face_box)
    result.save(img_path_final)


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
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    count = 0
    for (x, y, w, h) in faces:
        count += 1
        color = _random_bright_color()
        draw.rectangle(xy=[(x, y), (w, h)], outline=color, width=5)
        # font_size = int(min(w-x, h-y) / 30)  # TODO: make it relative
        font_path = os.path.join(settings.BASE_DIR, 'obfuscator', 'arial.ttf')
        font = ImageFont.truetype(font_path, size=30)
        draw.text(xy=(x + ((w-x) // 9 * 4), y), text=str(count), fill=color, font=font)
        # cv2.putText(img, str(count),
        #             (x + ((w-x) // 9 * 3), y - 5),
        #             fontFace=1,
        #             fontScale=fontScale,
        #             color=color,
        #             thickness=4,
        #             lineType=cv2.LINE_AA)

    # cv2.imwrite(img_path_final, img)
    img.save(img_path_final)
    faces_str = str(faces.tolist()) if len(faces) > 0 else "[]"
    return faces_str, count
    # to recover list of lists from the str:
    # new_faces = ast.literal_eval(faces_str)


def deepfake_and_number(img_path, img_path_final, faces_path):
    _resize_photo(img_path)
    faces = anonymize_and_get_faces(img_path, img_path_final)[0]
    faces_str, count = number_faces(img_path, faces_path, faces)
    return faces_str, count
