#localhost:5000/      used when wanting to ssee the website
# this is where you start!
from flask import Flask, render_template, request
from PIL import Image
import os

app = Flask(__name__, static_folder="static")

avner = {
    'name': 'Avner Biblars',
    'age': 30,
    'location': 'New York, NY',
    'interests': ['Music', 'Movies', 'Sports'],
    'profile_picture': 'avner.jpg',
    
    'background_music': 'music.mp3'
}
william = {
    'name': 'William Villantay',
    'age': 28,
    'location': 'California, CA',
    'interests': ['Games', 'Movies', 'Sleep'],
    'profile_picture': 'william.jpg',
    
    'background_music': 'music.mp3'
}

comments = []
# Load the image from the file
# Load the image from the file
def get_music_files():
    music_folder = os.path.join(app.root_path, 'static', 'music')
    music_files = []
    for file in os.listdir(music_folder):
        if file.endswith('.mp3'):
            music_files.append(file)
    return music_files

@app.route('/')
def index():
    return render_template('index.html', william=william, comments=comments, musics=get_music_files())


@app.route('/profile')
def profile():
    profile = 'avner.png'
    image = Image.open('static/images/' + profile)
    filter_value = request.args.get('filter', 'none')
    print(filter_value)
    if filter_value == "sepia":
        image = image.convert("RGB")
        sepia = image.convert("RGB")
        width, height = image.size
        for x in range(width):
            for y in range(height):
                r, g, b = image.getpixel((x, y))
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                if tr > 255:
                    r = 255
                if tg > 255:
                    g = 255
                if tb > 255:
                    b = 255
                sepia.putpixel((x, y), (tr, tg, tb))
        image = sepia
        image.save('static/images/' + 'avner.jpg')

    elif filter_value == "negative":
        image = image.convert("RGB")
        negative = image.convert("RGB")
        width, height = image.size
        for x in range(width):
            for y in range(height):
                r, g, b = image.getpixel((x, y))
                negative.putpixel(
                    (x, y), (255 - r, 255 - g, 255 - b))
        image = negative
        image.save('static/images/' + 'avner.jpg')
    elif filter_value == "grayscale":
        converted_image = image.convert("L")
        image = converted_image
        image.save('static/images/' + 'avner.png')
    elif filter_value == "thumbnail":
        image.thumbnail((100, 100))
        image.save('static/images/' + 'avner.jpg')
    else:
        filter_value = "none"
    
    return render_template('profile.html', user=avner, comments=comments, filter_value=filter_value)


@app.route('/upload_background', methods=['POST'])
def upload_background():
    file = request.files['file']
    filename = 'background.jpg'
    file.save('static/images/' + filename)
    return 'success'


@app.route('/upload_picture', methods=['POST'])
def upload_picture():
    file = request.files['file']
    filename = 'william.jpg'
    file.save('static/images/' + filename)
    return 'success'


@app.route('/post_comment', methods=['POST'])
def post_comment():
    comment = request.form['comment']
    comments.append(comment)
    return 'success'


if __name__ == '__main__':
    app.run(debug=True)
