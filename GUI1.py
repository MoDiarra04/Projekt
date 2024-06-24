import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Toplevel, filedialog, messagebox, ttk, Label
from Profilklasse1 import ProfileCard, clicked_profiles
from Datenbank import save_profile, get_profiles, delete_profile, update_selection, update_modulnummer

# Initialisierung der Auswahl(angeklickten Profile zum Tracken der Auswahl in profil laden)
selection = []
# alte Profile-Liste bzw. die geladenen Profile
active_profiles = []
# counter, ob active_profiles schon wiederhergestellt wurde
count = 0 

# old wiederherstellen, aber nur einmal
def recreate_old(profiles):
    global count
    if count == 1:
        return
    count += 1
    global active_profiles
    for tup in profiles:
        if tup[5] == 1:
            active_profiles.append(tup)

def create_main_page(app):
    # Firmenname-Label erstellen und platzieren
    firmenname_label = tk.Label(app, text="GreenTech Solutions", font=("Helvetica", 20), fg='green')
    firmenname_label.pack(side=tk.TOP)
    
    # Wochenansicht-Frame erstellen und konfigurieren
    app.wochenansicht_frame = tk.Frame(app, bg='grey', bd=5, relief="raised", pady=2)
    app.wochenansicht_frame.pack(side=tk.TOP)
    app.days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    for idx, day in enumerate(app.days):
        tk.Label(app.wochenansicht_frame, text=day).grid(row=0, column=idx, padx=5, pady=5)
    
    # Frame für die Buttons erstellen
    buttons_frame = tk.Frame(app)
    buttons_frame.pack(side=tk.RIGHT)
    
    # Button zum Erstellen eines Profils erstellen
    profil_erstellen_button = tk.Button(buttons_frame, text="Profil erstellen", command=lambda: create_profile_page(app))
    profil_erstellen_button.pack(side=tk.TOP)
    
    # Button zum Anzeigen der Profile erstellen
    profil_laden_button = tk.Button(buttons_frame, text="Profile anzeigen", command=lambda: show_profiles_page(app))
    profil_laden_button.pack(side=tk.TOP)
    manual_button = tk.Button(buttons_frame, text="Manuell", command= app.create_manual_page)
    manual_button.pack(pady=20)
    

def display_profiles(app, modulnummer=None):
    if count == 1:
        if not selection:
            messagebox.showerror("Sie müssen ein Profil auswählen")
            return

    if not modulnummer:
        print(clicked_profiles)
        messagebox.showerror("Sie müssen ein Modul auswählen")
        return
    
    profiles = get_profiles(app.conn)
    recreate_old(profiles)
    if selection != []:
        # Termine für Pflanze aus Datenbank filtern mithilfe des Namens 
        profile = [item for item in profiles if item[0] == selection[-1][0]]
        # Überprüfen ob Profil schon in old ist, falls nicht wird gepusht
        if not any(item[0] == profile[0][0] for item in active_profiles):
            update_modulnummer(app.conn,profile[0][0],modulnummer)
            #wegen update veränder sich profile, deshalb nochmal connecten
            profiles = get_profiles(app.conn)
            profile = [item for item in profiles if item[0] == selection[-1][0]] 
            for termine in profile:
                active_profiles.append(termine)


    profiles = active_profiles
    # Zuordnung der Profile zu den jeweiligen Wochentagen
    day_profile_map = {day: [] for day in app.days}
    for profile in profiles:
        name, wochentag, uhrzeit, bewaessungsdauer, _ , _ , modulnummer, smart = profile
        day_profile_map[wochentag].append((name, uhrzeit, bewaessungsdauer, modulnummer,smart))
    
    # Profile in der Wochenansicht anzeigen
    for day, profiles in day_profile_map.items():
        day_index = app.days.index(day)
        for i, (name, uhrzeit, bewaessungsdauer, modulnummer,smart) in enumerate(profiles):
            profile_frame = tk.Frame(app.wochenansicht_frame, bg="white", bd=2, relief="solid")
            profile_frame.grid(row=i + 1, column=day_index, padx=5, pady=5, sticky="nsew")
            profile_label = tk.Label(profile_frame, text=f"Pflanze: {name}\nUhrzeit: {uhrzeit} Uhr\nDauer: {bewaessungsdauer}min\nModul: {modulnummer}\nModus: {'Smart' if smart == 1 else 'Standard'}")
            profile_label.pack(padx=5, pady=5)
    
    # Selected in Datenbank ändern für Profile in old
    sorted = {item[0]: item for item in active_profiles}.values()
    for profile in sorted:
        update_selection(app.conn,profile[0],True)


def create_profile_page(app):
    app.image_path = None
    create_profile_window = Toplevel()
    create_profile_window.geometry("800x480")
    # Entfernt die title bar
    create_profile_window.overrideredirect(True)
    
    # Widgets für die Profilerstellung
    name_label = tk.Label(create_profile_window, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(create_profile_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
    
    bild_label = tk.Label(create_profile_window, text="Bild hochladen:")
    bild_label.grid(row=1, column=0, padx=10, pady=5)
    upload_button = tk.Button(create_profile_window, text="Bild hochladen", command=lambda: [set_image_path(app), raise_above_all(create_profile_window)])
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
    
    # Dropdown Dauer
    minuten_label = tk.Label(create_profile_window, text="Bewässerungsdauer (min):")
    minuten_label.grid(row=5, column=0, padx=10, pady=5)
    minutes = [str(minute) for minute in range(1, 21)]
    selected_minute = tk.StringVar()
    selected_minute.set(minutes[0])  # Standardmäßig die erste Minute auswählen
    minute_dropdown = tk.OptionMenu(create_profile_window, selected_minute, *minutes)
    minute_dropdown.grid(row=5, column=1, padx=10, pady=5)

    app.smart_button = tk.Button(create_profile_window, text="Smart", command=lambda: toggle_smart_button(app))
    app.smart_button.grid(row=6, column=0, columnspan=2, pady=10)
    update_smart_button_appearance(app)


    #Profile speichern    
    speichern_button = tk.Button(create_profile_window, text="Speichern", command=lambda: save_profile_and_close(app, name_entry.get(), selected_weekday, selected_hour, selected_minute, app.smart_button_active))

    speichern_button.grid(row=7, column=0, columnspan=2, pady=10)
    
    # Back button
    back_button = tk.Button(create_profile_window, text="Zurück", command=create_profile_window.destroy)
    back_button.grid(row=7, column=1, pady=10)

def save_profile_and_close(app, name, weekday, hour, duration_entry, smart):
    # Validierung der Eingaben
    if  not weekday.get() or not hour.get() or not duration_entry.get():
        messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt werden!")
        return
    image_path = app.image_path if app.image_path else Default_Image
    name = name if name else "Pflanze"
    # Speichern des Profils in der Datenbank
    save_profile(app.conn, name, weekday.get(), hour.get(), duration_entry.get(), image_path, False,False, smart)
    
    # Setzen der nächsten Eingabefelder
    current_day_index = app.days.index(weekday.get())
    next_day_index = (current_day_index + 1) % len(app.days)
    next_day = app.days[next_day_index]
    weekday.set(next_day)
    
    hour.set("00:00")


def show_profiles_page(app):
    create_window = tk.Toplevel(app)
    create_window.geometry("800x480")
    create_window.title("Profiles")
    # Entfernt die title bar
    create_window.overrideredirect(True)

    
    # Frame und Canvas für die Profilansicht erstellen
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
    
    # Profile aus der Datenbank holen und anzeigen
    profiles = get_profiles(app.conn)
    profiles = {item[0]: item for item in profiles}.values()
    for profile in profiles:
        card = ProfileCard(profiles_frame, profile, update_callback=update_clicked_profiles)
        card.pack(padx=10, pady=10, fill="x")
    
    # Checkbox erstellen
    module_var = tk.StringVar()  # Gemeinsame Variable für beide Checkbuttons
    module_checkbox1 = tk.Checkbutton(create_window, text="Pumpe: 1", variable=module_var, onvalue="1", offvalue="")
    module_checkbox1.pack(side="left", padx=10)
    module_checkbox2 = tk.Checkbutton(create_window, text="Pumpe: 2", variable=module_var, onvalue="2", offvalue="")
    module_checkbox2.pack(side="left", padx=10)

    # Button-Frame erstellen
    button_frame = tk.Frame(create_window)
    button_frame.pack(fill="x", pady=10)
    
    back_button = tk.Button(button_frame, text="Zurück", command=create_window.destroy)
    back_button.pack(side="left", padx=5)
    edit_button = tk.Button(button_frame, text="Edit", command=edit_profile)
    edit_button.pack(side="left", padx=5)
    exp_button = tk.Button(button_frame, text="Export")
    exp_button.pack(side="left", padx=5)
    imp_button = tk.Button(button_frame, text="Import")
    imp_button.pack(side="left", padx=5)
    ok_button = tk.Button(button_frame, text="OK", command=lambda: [ok_button_callback(app,module_var,create_window),selection.clear()])
    ok_button.pack(side="right", padx=5)

def ok_button_callback(app,module_var,create_window):
    # Check if the module_var is not empty before converting to int
    if module_var.get():
        selected_module = int(module_var.get())
        display_profiles(app, selected_module)
    
    create_window.destroy()

def update_clicked_profiles(profiles):
    global selection
    for profile in clicked_profiles:
        selection.append(profile)
    clicked_profiles.clear()
    clicked_profiles.extend(profiles)

Default_Image = "Projekt\pflanze.png"

def set_image_path(app):
    file_path = filedialog.askopenfilename()
    if file_path:
        app.image_path = file_path
        img = Image.open(file_path)
        img.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(img)
        app.image_label.config(image=photo)
        app.image_label.image = photo
    else:
        app.image_path = Default_Image


# Variablen zum Speichern des after-ID-Objekts und der verbleibenden Zeit
after_id = None
remaining_time = 0
original_duration = 0

def create_manual_page(app):
    global remaining_time, original_duration

    # Reset the selected time and remaining time when opening the window
    selected_time = tk.IntVar(value=1)  # Set initial value to 1
    
    choices = [int(i) for i in range(1, 21)]
    
    # Create a window for manual watering
    manual_window = Toplevel(app)
    manual_window.title("Manuelle Bewässerung")
    dauer_label = tk.Label(manual_window, text="Bewässerungsdauer (Minuten):")
    dauer_label.grid(row=0, column=0, padx=10, pady=5)
    
    drop = ttk.Combobox(manual_window, textvariable=selected_time, values=choices, state="readonly")
    drop.grid(row=0, column=1, padx=10, pady=5)
    drop.bind("<<ComboboxSelected>>", lambda event: update_duration(selected_time.get()))

    start_button = tk.Button(manual_window, text="Starten", command=lambda: start_countdown(app, manual_window, start_button, drop, countdown_label))
    start_button.grid(row=1, column=0, columnspan=2, pady=10)
    
    back_button = tk.Button(manual_window, text="Zurück", command=lambda: close_manual_window(app, manual_window))
    back_button.grid(row=1, column=1, columnspan=2, pady=10)
    
    countdown_label = tk.Label(manual_window, text="")
    countdown_label.grid(row=2, column=0, columnspan=2, pady=10)

def update_duration(duration):
    global remaining_time, original_duration
    remaining_time = duration * 60
    original_duration = remaining_time

def start_countdown(app, window, button, drop, label):
    global after_id, remaining_time, original_duration

    if remaining_time == 0:
        remaining_time = original_duration

    if after_id is not None:
        app.after_cancel(after_id)

    after_id = update_countdown(app, label, button, drop)
    
    # Change to stop button
    button.config(text="Stopp", command=lambda: stop_countdown(app, button, label, drop))

def stop_countdown(app, button, label, drop):
    global after_id

    # Stop the countdown and change the button back to start
    if after_id:
        app.after_cancel(after_id)
        after_id = None
    label.config(text="Gestoppt")
    button.config(text="Starten", command=lambda: start_countdown(app, button.master, button, drop, label))

def update_countdown(app, label, button, drop):
    global after_id, remaining_time
    
    # Update the countdown timer
    if remaining_time > 0:
        minutes, seconds = divmod(remaining_time, 60)
        label.config(text=f"Verbleibende Zeit: {minutes} Minuten {seconds} Sekunden")
        after_id = app.after(1000, update_countdown, app, label, button, drop)
        remaining_time -= 1
    else:
        label.config(text="Bewässerung abgeschlossen!")
        button.config(text="Starten", command=lambda: start_countdown(app, original_duration // 60, button.master, button, drop, label))
        after_id = None

def close_manual_window(app, window):
    global after_id
    if after_id is not None:
        app.after_cancel(after_id)
        after_id = None
    window.destroy()

# Smart-Button-Konfiguration
def toggle_smart_button(app):
    # Wechselt den Status des Smart-Buttons
    app.smart_button_active = not app.smart_button_active
    update_smart_button_appearance(app)

def update_smart_button_appearance(app):
    # Aktualisiert das Erscheinungsbild des Smart-Buttons
    if app.smart_button_active:
        app.smart_button.config(bg='green', text='Smart (Aktiv)')
    else:
        app.smart_button.config(bg='SystemButtonFace', text='Smart')



def edit_profile(app):

   
    newWindow = Toplevel()

    newWindow.title("Profil Bearbeiten")

    newWindow.geometry("800x480")
    
    
    name_label = tk.Label(newWindow, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(newWindow)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
    
    bild_label = tk.Label(newWindow, text="Bild hochladen:")
    bild_label.grid(row=1, column=0, padx=10, pady=5)
    upload_button = tk.Button(newWindow, text="Bild hochladen", command=lambda: [set_image_path(), raise_above_all()])
    upload_button.grid(row=1, column=1, padx=10, pady=5)
    
    image_label = tk.Label(newWindow)
    image_label.grid(row=2, column=1, padx=10, pady=5)
    
    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    weekday_label = tk.Label(newWindow, text="Wochentag:")
    weekday_label.grid(row=3, column=0, padx=10, pady=5)
    selected_weekday = tk.StringVar(value=weekdays[0])
    weekday_dropdown = tk.OptionMenu(newWindow, selected_weekday, *weekdays)
    weekday_dropdown.grid(row=3, column=1, padx=10, pady=5)
    
    hours = [f"{hour:02d}:00" for hour in range(24)]
    selected_hour_label = tk.Label(newWindow, text="Uhrzeit:")
    selected_hour_label.grid(row=4, column=0, padx=10, pady=5)
    selected_hour = tk.StringVar(value=hours[0])
    hour_dropdown = tk.OptionMenu(newWindow, selected_hour, *hours)
    hour_dropdown.grid(row=4, column=1, padx=10, pady=5)
    
    # Dropdown Dauer
    minuten_label = tk.Label(newWindow, text="Bewässerungsdauer (min):")
    minuten_label.grid(row=5, column=0, padx=10, pady=5)
    minutes = [str(minute) for minute in range(1, 21)]
    selected_minute = tk.StringVar()
    selected_minute.set(minutes[0])  # Standardmäßig die erste Minute auswählen
    minute_dropdown = tk.OptionMenu(newWindow, selected_minute, *minutes)
    minute_dropdown.grid(row=5, column=1, padx=10, pady=5)

    smart_button = tk.Button(newWindow, text="Smart", command=lambda: toggle_smart_button(app))
    smart_button.grid(row=6, column=0, columnspan=2, pady=10)
    update_smart_button_appearance()

   


    
def raise_above_all(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)