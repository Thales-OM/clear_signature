import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps
import os

def transform_image(image):
    # Apply the transformation to extract the signature lines
    threshold = 128
    transformed_image = image.point(lambda pixel: 255 if pixel > threshold else 0)
    return transformed_image

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    image = Image.open(file_path).convert('L')
    transformed_image = transform_image(image)
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    save_image_locally(transformed_image, save_path)

def save_image_locally(image, save_path):
    abs_dir_path = os.path.dirname(os.path.abspath(save_path))
    
    if not os.path.exists(abs_dir_path):
        os.makedirs(abs_dir_path, exist_ok=True)

    image.save(save_path)

def main():
    root = tk.Tk()
    root.title("Signature Extraction App")

    open_button = tk.Button(root, text="Open Image", command=open_image)
    open_button.pack()

    root.mainloop()

if __name__ == '__main__':
    main()