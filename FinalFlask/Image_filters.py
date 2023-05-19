from re import X
from tkinter import Y
from PIL import Image, ImageFilter, ImageEnhance
import random
import os
import numpy as np
import cv2
from flask import Flask, render_template, flash, redirect, url_for, Response, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import FileField, SelectField
from wtforms.validators import DataRequired
import base64
import io

#collection of Image_Filters
def apply_image_filter(img, filter_name):
    if filter_name == 'negative':
        img = negative_filter(img)
    elif filter_name == 'grayscale':
        img = grayscale_filter(img)
    elif filter_name == 'mosaic':
        img = mosaic_filter(img)
    elif filter_name == 'sketch':
        img = sketch_filter(img)
    elif filter_name == 'sobel':
        img = sobel_filter(img)
    return img

#Profile image editing
def negative_filter(img):
    pix_change = [(255-p[0], 255-p[1], 255-p[2]) for p in img.getdata()]
    img.putdata(pix_change)
    return img

def grayscale_filter(img):
    pix_changes = [((p[0]+p[1]+p[2] // 3) / 2) for p in img.getdata()]
    new_img = Image.new("L", img.size)
    new_img.putdata(pix_changes)
    return new_img

def mosaic_filter(img):
    small_img = img.resize((50,50))
    new_img = small_img.resize(img.size, Image.NEAREST)
    return new_img

def sketch_filter(img):
    # reading img to turn into a CV image
    cv_img = np.asarray(img) 
    #turn img gray
    gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    #invert the colors
    invert_img = cv2.bitwise_not(cv_img)
    #blur image to get better line dectection
    blur_img = cv2.GaussianBlur(invert_img, (21, 21), 0)
    # inverting the blurred img
    invertedblur_img = cv2.bitwise_not(blur_img)
    # turn blur image into gray img bc it was not a gray img?
    invertedblur_img = cv2.cvtColor(invertedblur_img, cv2.COLOR_BGR2GRAY)
    # putting it all together
    sketch_img = cv2.divide(gray_img, invertedblur_img, scale=256.0)
    # turning the image array into a PIL img
    new_img = Image.fromarray(sketch_img)
    return new_img

def sobel_filter(img):
    # reading img to turn into a CV image
    cv_img = np.asarray(img) 
    #turn img gray
    gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    #blur image to get better line dectection
    blur_img = cv2.GaussianBlur(gray_img, (3, 3), 0)
    #edge detection on the x-axis
    x = cv2.Sobel(blur_img, cv2.CV_64F, 1, 0, 5)
    new_img = Image.fromarray(x)
    return new_img

# Setting up page
app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)

#user img
class User_image(FlaskForm):
    user_img = FileField(validators=[DataRequired()])
    filter = SelectField('Filter', choices =[('negative', 'Negative Filter'), ('grayscale', 'Grayscale Filter'),
                                            ('mosaic', 'Mosaic Filter'), ('sketch', 'Sketch Filter'),
                                            ('sobel', 'Sobel Filter')], validators=[DataRequired()])

@app.route('/',methods=['POST','GET'])
def text_page():
    form = User_image()

    if form.validate_on_submit():
        image_file = form.user_img.data
        image = Image.open(image_file)
        filter_name = form.filter.data

        # Apply the selected filter to the image
        processed_image = apply_image_filter(image, filter_name)

        # Convert the processed image to base64 string for display
        buffered = io.BytesIO()
        processed_image.save(buffered, format='JPEG')
        encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return render_template('profile_image.html', form=form, image_data=encoded_image)

    return render_template('profile_image.html', form=form)
