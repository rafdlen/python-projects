import zipfile
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFont, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np

# asking user for word to search
q = input("Type one word to initiate search: ")

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# assigning zip file to the variable
zip_file = "readonly/images.zip"

# creating list of names of img files in zip file
images_names_list = []

# opening zip_file and extracting zip_file, populating images_names_list
with zipfile.ZipFile(zip_file, "r") as file:
    for img in file.namelist():
        images_names_list.append(img)
    file.extractall()

# running tesseract on images in images_list, appending images, that match the query to a new list
img_with_searched_word = []
for img in images_names_list:
    text = pytesseract.image_to_string(img)
    if q in text:
        img_with_searched_word.append(img)


# detecting faces with opencv
for img in img_with_searched_word:
    image = cv.imread(img)
    gray = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    faces = face_cascade.detectMultiScale(image,
    scaleFactor=1.2,
    minNeighbors=5,
    minSize=(40, 40),
    flags=cv.CASCADE_SCALE_IMAGE)

    print("Found {0} faces!".format(len(faces)))

    # creating list of faces in np format
    list_of_faces = []
    for (x, y, w, h) in faces:
        cv.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 2)
        faces = gray[y:y + h, x:x + w]
        list_of_faces.append(faces)


    #creating list of PIL images for making a contact sheet
    list_of_PIL_img = []
    for im in list_of_faces:
        fb = Image.fromarray(im)
        list_of_PIL_img.append(fb)


    # creating a contact sheet
    if len(list_of_PIL_img) > 0:
        first_image = list_of_PIL_img[0]
        contact_sheet = Image.new(first_image.mode, (first_image.width*3,first_image.height*3+3*85))
        x = 0
        y = 0
        draw_cs = ImageDraw.Draw(contact_sheet)

        # pasting the current image into the contact sheet
        for i, img in enumerate(list_of_PIL_img):
            contact_sheet.paste(img, (x, y))
            if x+first_image.width == contact_sheet.width:
                x=0
                y=y+first_image.height
            else:
                x=x+first_image.width

            # displaying contact sheet
        contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
        display(contact_sheet)
    else:
        print("But there were no faces in that file!")



