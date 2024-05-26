import tkinter as tk
from PIL import Image, ImageTk

# Liste der angeklickten Profile initialisieren
clicked_profiles = []

class ProfileCard(tk.Frame):
    def __init__(self, parent, profile, update_callback=None):
        super().__init__(parent, bg="white", bd=2, relief="solid")
        self.profile = profile
        self.selected = False
        self.update_callback = update_callback
        self.create_widgets_with_image(parent)

    def create_widgets_with_image(self, window):
        name = self.profile[0]
        image_path = self.profile[-1]
        
        # Wenn ein Bildpfad vorhanden ist, das Bild laden und anzeigen
        if image_path:
            image = Image.open(image_path)
            image.thumbnail((150, 150))
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(window, image=photo, bg="white")
            image_label.image = photo  # Referenz speichern, um das Bild anzuzeigen
            image_label.pack()

        # Label mit dem Profilnamen erstellen und anzeigen
        name_label = tk.Label(window, text=name, bg="white", font=("Helvetica", 12))
        name_label.pack(padx=5, pady=5)
        
        # Klick-Ereignis an das Namenslabel binden
        name_label.bind("<Button-1>", self.on_click)
        self.pack_propagate(False)

    def on_click(self, event):
        # Umschalten des ausgewählten Status
        self.selected = not self.selected
        
        # Profil zur Liste der angeklickten Profile hinzufügen oder entfernen
        if self.selected:
            clicked_profiles.append(self.profile)
            self.config(bg="lightgreen")
        else:
            clicked_profiles.remove(self.profile)
            self.config(bg="white")
        
        # Wenn ein Update-Callback bereitgestellt wurde, diesen aufrufen
        if self.update_callback:
            self.update_callback(clicked_profiles)
