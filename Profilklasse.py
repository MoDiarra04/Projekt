import tkinter as tk
from PIL import Image, ImageTk

class Card(tk.Frame):
    def __init__(self, parent, image_path="", pflanze="",tag="", uhrzeit="",dauer=""):
        super().__init__(parent)
        self.image_path = image_path
        self.pflanze = pflanze
        
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        if self.image_path:
            image = Image.open(self.image_path)
            image.thumbnail((150, 150))
            photo = ImageTk.PhotoImage(image)

            self.image_label = tk.Label(self, image=photo)
            self.image_label.image = photo
            self.image_label.pack()

        if self.pflanze:
            self.pflanze_label = tk.Label(self, text=self.pflanze)
            self.pflanze_label.pack()

root = tk.Tk()
root.title("Card Example")

# Prompt user to enter image path and text for the card
image_path = "C:\\Users\\Asus\\Desktop\\Code\\Projekt\\Projekt\\Icon.png"
pflanze = "Icon"

card = Card(root, image_path, pflanze)
card2 = Card(root, image_path, pflanze)

root.mainloop()
