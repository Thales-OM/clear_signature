from flask import Flask, render_template, request
from PIL import Image, ImageOps
import os

# from image_transform import transform_image, save_image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    if file:
        image = Image.open(file).convert('L')
        transformed_image = transform_image(image)
        save_image(transformed_image)
        return "Image processed and saved successfully!"
    else:
        return "Error: No image file received"

def transform_image(image):
    # Apply the transformation to extract the signature lines
    threshold = 128
    transformed_image = image.point(lambda pixel: 255 if pixel > threshold else 0)
    return transformed_image

def save_image(image):
    save_path = 'static/transformed_image.png'
    abs_dir_path = os.path.dirname(os.path.abspath(save_path))
    
    if not os.path.exists(abs_dir_path):
        os.makedirs(abs_dir_path, exist_ok=True)
    
    image.save(save_path)

if __name__ == '__main__':
    app.run(debug=True)