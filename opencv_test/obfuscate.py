import cv2
import imutils


def apply_blur(image, factor=3.0):
	# automatically determine the size of the blurring kernel based
	# on the spatial dimensions of the input image
    h, w, _ = image.shape
    kW = int(w / factor)
    kH = int(h / factor)

    # ensure the width and height of the kernel are odd
    kW -= 1 if kW % 2 == 0 else kW
    kH -= 1 if kH % 2 == 0 else kH

    return cv2.GaussianBlur(image, (kW, kH), sigmaX=0)


def pixelate(image):
    h, w, _ = image.shape
    w_pixel, h_pixel = (w//5, h//5)
    # Resize input to "pixelated" size
    temp = cv2.resize(image, dsize=(w_pixel, h_pixel), interpolation=cv2.INTER_NEAREST)
    cv2.imshow("img", temp)
    cv2.waitKey()
    return cv2.resize(temp, dsize=(w, h), interpolation=cv2.INTER_NEAREST)


def _get_faces(img):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(image=gray, scaleFactor=1.4, minNeighbors=5)


if __name__ == "__main__":

    img = cv2.imread('friends-2.jpg') # ('pexels-nathan-cowley-1300402.jpg')
    img = imutils.resize(img, width=500)

    faces = _get_faces(img)
    for (x, y, w, h) in faces:
        region_of_interest = img[y:y+h, x:x+w]
        # pixelated_roi =  pixelate(region_of_interest)
        # img[y:y+h, x:x+w] = pixelated_roi
        img[y:y+h, x:x+w] = apply_blur(region_of_interest)
        #cv2.rectangle(img, (x, y), (x+w, y+h), color=(255, 0, 0), thickness=2)

    cv2.imshow("img", img)
    cv2.waitKey()
