import math
import zipfile
import numpy
import pytesseract
import cv2 as cv

from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('readonly/haarcascade_eye.xml')


# Your task is to write python code which allows one to
# search through the images looking for the occurrences of keywords and faces. E.g.
# if you search for "pizza" it will return a contact sheet of all of the faces
# which were located on the newspaper page which mentions "pizza".
#
# This will test your ability to learn a new (library),
# your ability to use OpenCV to detect faces,
# your ability to use tesseract to do optical character recognition,
# and your ability to use PIL to composite images together into contact sheets.


class ImageData:

    def __init__(self, image, fileName, text):
        self.image = image
        self.fileName = fileName
        self.text = text


def loadZipFile(zipFilePath, dataSet):
    # start to process the zipfile
    zf = zipfile.ZipFile(zipFilePath)
    print("start processing")
    for fileInfo in zf.infolist():
        singleFile = zf.open(fileInfo)

        print("processing " + fileInfo.filename)
        img = Image.open(singleFile).convert('RGB')
        # img_cv = cv.imread(singleFile)
        fileName = fileInfo.filename
        text = pytesseract.image_to_string(img).replace('-\n', '')

        dataSet.append(ImageData(img, fileName, text))
    print("finished processing")


def findFaces(image):
    cv_img = cv.cvtColor(numpy.array(image), cv.COLOR_RGB2BGR)
    facesIndex = face_cascade.detectMultiScale(cv_img, 1.3, 5)
    faces = []
    for x, y, w, h in facesIndex:
        faces.append(image.crop((x, y, x + w, y + h)))
    if len(faces) == 0:
        return None
    h = math.ceil(len(faces) / 5)
    contact_sheet = Image.new('RGB', (500, 100 * h))
    x = 0
    y = 0
    for img in faces:
        img.thumbnail((100, 100))
        contact_sheet.paste(img, (x, y))
        if x + 100 == contact_sheet.width:
            x = 0
            y += 100
        else:
            x += 100
    return contact_sheet


def search(targetText):
    for imageData in DataSet:
        if targetText not in imageData.text:
            continue
        print("Result found in file {}".format(imageData.fileName))
        res = findFaces(imageData.image)
        if res is None:
            print("But there were no faces in that file!")
        else:
            res.show()


# ---------------------------
# main function of this task
# ---------------------------

DataSet = []

# loadZipFile('readonly/small_img.zip', DataSet)
loadZipFile('readonly/images.zip', DataSet)

for data in DataSet:
    print(data.fileName)

print("---------------------")
search('Mark')
