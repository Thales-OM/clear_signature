from flask import Flask, render_template, request, send_file
from PIL import Image, ImageOps
import os

from image_transformer import transform_image, save_image_locally


############### CONFIG ###################
IMAGE_STORE_DIR_PATH = 'static'
##########################################


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    save_path = get_image_save_path()

    if file and save_path:
        image = Image.open(file).convert('L')
        transformed_image = transform_image(image)
        save_image_locally(transformed_image, save_path)
        
        return send_file(save_path, as_attachment=True)
    else:
        return "Error: No image file or save path received"

def get_image_save_path():
    filename = 'processed_image.jpeg'
    return os.path.join(IMAGE_STORE_DIR_PATH, filename)

if __name__ == '__main__':
    app.run(debug=True)