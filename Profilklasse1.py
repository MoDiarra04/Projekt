import os
from PIL import Image, ImageTk
import tkinter as tk

class ProfileCard(tk.Frame):
    def __init__(self, parent, profile, show_image=False):
        super().__init__(parent, bg="white", bd=2, relief="solid")
        self.profile = profile
        self.show_image = show_image
        if self.show_image == True:
            self.create_widgets2()
        else:
            self.create_widgets1()

    def create_widgets1(self):
        name, wochentag, uhrzeit, bewaessungsdauer = self.profile

        profile_label = tk.Label(self, text=f"{name}\n{wochentag} {uhrzeit}\n{bewaessungsdauer} min", bg="white")
        profile_label.pack(padx=5, pady=5)
    
    def create_widgets2(self):
        name, wochentag, uhrzeit, bewaessungsdauer, image_path = self.profile

        
        image = Image.open(image_path)
        image.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(self, image=photo, bg="white")
        image_label.image = photo
        image_label.pack()

        self.pack_propagate(False)
