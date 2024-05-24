import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Toplevel, filedialog, messagebox
from Profilklasse1 import ProfileCard,clicked_profiles
from Datenbank import save_profile, get_profiles, delete_profile  # Import "Datenbank" könnte nicht aufgelöst werden

selection=[]
old = []

def create_main_page(app):
    firmenname_label = tk.Label(app, text="Firmenname", font=("Helvetica", 20))
    firmenname_label.pack(side=tk.TOP)
    
    app.wochenansicht_frame = tk.Frame(app, bg='grey', bd=5, relief="raised", pady=2)
    app.wochenansicht_frame.pack(side=tk.TOP)
    app.days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    for idx, day in enumerate(app.days):
        tk.Label(app.wochenansicht_frame, text=day).grid(row=0, column=idx, padx=5, pady=5)
    
    buttons_frame = tk.Frame(app)
    buttons_frame.pack(side=tk.RIGHT)
    
    profil_erstellen_button = tk.Button(buttons_frame, text="Profil erstellen", command=lambda: create_profile_page(app))
    profil_erstellen_button.pack(side=tk.TOP)
    
    profil_laden_button = tk.Button(buttons_frame, text="Profile anzeigen", command=lambda: show_profiles_page(app))
    profil_laden_button.pack(side=tk.TOP)

def display_profiles(app):
    for widget in app.wochenansicht_frame.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()
    
    profiles = get_profiles(app.conn)
    if selection != []:
        profiles = [item for item in profiles if item[0] == selection[-1][0]]
        global old
        if not any(item[0]==profiles[0][0] for item in old):
            for profile in profiles:
                old.append(profile)
    print(old)
    profiles = old
    day_profile_map = {day: [] for day in app.days}
    for profile in profiles:
        name, wochentag, uhrzeit, bewaessungsdauer, _ = profile
        day_profile_map[wochentag].append((name, uhrzeit, bewaessungsdauer))
    
    for day, profiles in day_profile_map.items():
        day_index = app.days.index(day)
        for i, (name, uhrzeit, bewaessungsdauer) in enumerate(profiles):
            profile_frame = tk.Frame(app.wochenansicht_frame, bg="white", bd=2, relief="solid")
            profile_frame.grid(row=i + 1, column=day_index, padx=5, pady=5, sticky="nsew")
            profile_label = tk.Label(profile_frame, text=f"{name}\n{uhrzeit}\n{bewaessungsdauer}")
            profile_label.pack(padx=5, pady=5)

def create_profile_page(app):
    app.image_path = None
    create_profile_window = Toplevel()
    create_profile_window.title("Profil erstellen")
    
    name_label = tk.Label(create_profile_window, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(create_profile_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
    
    bild_label = tk.Label(create_profile_window, text="Bild hochladen:")
    bild_label.grid(row=1, column=0, padx=10, pady=5)
    upload_button = tk.Button(create_profile_window, text="Bild hochladen", command=lambda: set_image_path(app))
    upload_button.grid(row=1, column=1, padx=10, pady=5)
    
    app.image_label = tk.Label(create_profile_window)
    app.image_label.grid(row=2, column=1, padx=10, pady=5)
    
    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    weekday_label = tk.Label(create_profile_window, text="Wochentag:")
    weekday_label.grid(row=3, column=0, padx=10, pady=5)
    selected_weekday = tk.StringVar(value=weekdays[0])
    weekday_dropdown = tk.OptionMenu(create_profile_window, selected_weekday, *weekdays)
    weekday_dropdown.grid(row=3, column=1, padx=10, pady=5)
    
    hours = [f"{hour:02d}:00" for hour in range(24)]
    selected_hour_label = tk.Label(create_profile_window, text="Uhrzeit:")
    selected_hour_label.grid(row=4, column=0, padx=10, pady=5)
    selected_hour = tk.StringVar(value=hours[0])
    hour_dropdown = tk.OptionMenu(create_profile_window, selected_hour, *hours)
    hour_dropdown.grid(row=4, column=1, padx=10, pady=5)
    
    dauer_label = tk.Label(create_profile_window, text="Bewässerungsdauer (min):")
    dauer_label.grid(row=5, column=0, padx=10, pady=5)
    dauer_entry = tk.Entry(create_profile_window)
    dauer_entry.grid(row=5, column=1, padx=10, pady=5)
    
    speichern_button = tk.Button(create_profile_window, text="Speichern", command=lambda: save_profile_and_close(app, name_entry.get(), selected_weekday, selected_hour, dauer_entry, create_profile_window))
    speichern_button.grid(row=6, column=0, columnspan=2, pady=10)

def save_profile_and_close(app, name, weekday, hour, duration_entry, window):
    if not name or not app.image_path or not weekday.get() or not hour.get() or not duration_entry.get():
        messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt werden!")
        return
    
    save_profile(app.conn, name, weekday.get(), hour.get(), duration_entry.get(), app.image_path)
    current_day_index = app.days.index(weekday.get())
    next_day_index = (current_day_index + 1) % len(app.days)
    next_day = app.days[next_day_index]
    weekday.set(next_day)
    
    hour.set("00:00")
    duration_entry.delete(0, tk.END)
    
def show_profiles_page(app):
    create_window = Toplevel(app)
    create_window.title("Profiles")
    
    container = tk.Frame(create_window)
    container.pack(fill="both", expand=True)
    
    canvas = tk.Canvas(container)
    canvas.pack(side="left", fill="both", expand=True)
    
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    profiles_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=profiles_frame, anchor="nw")
    
    profiles = get_profiles(app.conn)
    profiles = {item[0]: item for item in profiles}.values()
    for profile in profiles:
        card = ProfileCard(profiles_frame, profile, update_callback=update_clicked_profiles)
        card.pack(padx=10, pady=10, fill="x")
    
    button_frame = tk.Frame(create_window)
    button_frame.pack(fill="x", pady=10)
    
    back_button = tk.Button(button_frame, text="Back")
    back_button.pack(side="left", padx=5)
    edit_button = tk.Button(button_frame, text="Edit")
    edit_button.pack(side="left", padx=5)
    exp_button = tk.Button(button_frame, text="Export")
    exp_button.pack(side="left", padx=5)
    imp_button = tk.Button(button_frame, text="Import")
    imp_button.pack(side="left", padx=5)
    ok_button = tk.Button(button_frame, text="OK", command=lambda: display_profiles(app))
    ok_button.pack(side="right", padx=5)

def update_clicked_profiles(profiles):
    global selection
    for profile in clicked_profiles:
        selection.append(profile)
    clicked_profiles.clear()
    clicked_profiles.extend(profiles)

def set_image_path(app):
    file_path = filedialog.askopenfilename()
    if file_path:
        app.image_path = file_path
        img = Image.open(file_path)
        img.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(img)
        app.image_label.config(image=photo)
        app.image_label.image = photo


