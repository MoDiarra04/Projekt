import tkinter as tk
from tkinter import Toplevel
from Profilklasse1 import ProfileCard
from upload import upload_image
from Datenbank import save_profile, get_profiles, delete_profile


def create_main_page(app):
    firmenname_label = tk.Label(app, text="Firmenname", font=("Helvetica", 20))
    firmenname_label.pack(side=tk.TOP)

    app.wochenansicht_frame = tk.Frame(app, bg='grey', bd=5, relief="raised", pady=2)
    app.wochenansicht_frame.pack(side=tk.TOP)

    app.days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    for idx, day in enumerate(app.days):
        tk.Label(app.wochenansicht_frame, text=day).grid(row=0, column=idx, padx=5, pady=5)

    buttons_frame = tk.Frame(app)
    buttons_frame.pack(side=tk.RIGHT, padx=10, pady=10)
    profil_erstellen_button = tk.Button(buttons_frame, text="Profil erstellen", command=lambda: create_profile_page(app))
    profil_erstellen_button.pack(side=tk.TOP)
    profil_laden_button = tk.Button(buttons_frame, text="Profile anzeigen", command=lambda: show_profiles_page(app))
    profil_laden_button.pack(side=tk.TOP)

def display_profiles(app):
    for widget in app.wochenansicht_frame.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()

    profiles = get_profiles(app.conn)

    day_profile_map = {day: [] for day in app.days}
    for profile in profiles:
        name, wochentag, uhrzeit, bewaessungsdauer, _ = profile
        day_profile_map[wochentag].append((name, uhrzeit, bewaessungsdauer))

    for day, profiles in day_profile_map.items():
        day_index = app.days.index(day)
        for i, (name, uhrzeit, bewaessungsdauer) in enumerate(profiles):
            profile_frame = tk.Frame(app.wochenansicht_frame, bg="white", bd=2, relief="solid")
            profile_frame.grid(row=i + 1, column=day_index, padx=5, pady=5, sticky="nsew")
            profile_label = tk.Label(profile_frame, text=f"{name}\n{uhrzeit}\n{bewaessungsdauer} min", bg="white")
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
    upload_button = tk.Button(create_profile_window, text="Bild hochladen", command=lambda: set_image_path(app, create_profile_window))
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

    speichern_button = tk.Button(create_profile_window, text="Speichern", command=lambda: save_profile_and_close(app, name_entry.get(), selected_weekday.get(), selected_hour.get(), dauer_entry.get(), create_profile_window))
    speichern_button.grid(row=6, column=0, columnspan=2, pady=10)

def set_image_path(app, window):
    file_path = upload_image(window, app.image_label)
    if file_path:
        app.image_path = file_path

def save_profile_and_close(app, name, wochentag, uhrzeit, bewaessungsdauer, window):
    save_profile(app.conn, name, wochentag, uhrzeit, bewaessungsdauer, app.image_path)
    display_profiles(app)
    window.destroy()

def show_profiles_page(app):
    profiles_window = Toplevel()
    profiles_window.title("Profile anzeigen")

    profiles = sorted(get_profiles(app.conn), key=lambda x: x[0])

    row, col = 0, 0
    for profile in profiles:
        if col >= 4:
            col = 0
            row += 1

        card = ProfileCard(profiles_window, profile, show_image=True)
        card.grid(row=row, column=col, padx=5, pady=5)
        col += 1

    delete_button = tk.Button(profiles_window, text="Profil löschen", command=lambda: delete_selected_profile(app, profiles_window))
    delete_button.grid(row=row + 1, column=0, columnspan=4, pady=10)


def delete_selected_profile(app, window):
    selected_profile = None
    for widget in window.winfo_children():
        if isinstance(widget, ProfileCard) and widget.profile:
            selected_profile = widget.profile
            break

    if selected_profile:
        name = selected_profile[0]
        delete_profile(app.conn, name)
        window.destroy()
        show_profiles_page(app)
