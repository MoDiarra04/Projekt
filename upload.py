from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk

def upload_image(window, image_label):
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((150, 150))
        photo = ImageTk.PhotoImage(image)
        if image_label:
            image_label.config(image=photo)
            image_label.image = photo
        return file_path
    return None
