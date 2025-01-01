import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox


class WeatherApp:
    def __init__(self, master) -> None:
        self.master = master
        self.master.geometry("400x400")
        self.master.title("Weather App")

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)

        ttk.Label(self.master, text="Insert a town:", font=("Helvetica", 15)).grid(row=0, column=1, pady=10)

        self.entry_for_town = ttk.Entry(self.master, bootstyle=PRIMARY, width=25)
        self.entry_for_town.grid(row=1, column=1, padx=10, pady=10)

        # Menubutton for selecting temperature unit
        self.unit_selection = ttk.Menubutton(self.master, text="C / F", bootstyle=PRIMARY)
        self.unit_selection.grid(row=2, column=1, padx=10, pady=10)

        # Create a menu and associate it with the Menubutton
        self.unit_menu = ttk.Menu(self.unit_selection, tearoff=0)
        self.unit_selection["menu"] = self.unit_menu

        self.unit_menu.add_command(label="Celsius (C)", command=lambda: self.set_unit("C"))
        self.unit_menu.add_command(label="Fahrenheit (F)", command=lambda: self.set_unit("F"))

        self.selected_unit = "C"

        self.button_to_show_weather = ttk.Button(self.master, text="Show Weather", command=self.get_weather)
        self.button_to_show_weather.grid(row=3, column=1)

    def set_unit(self, unit):
        """Set the selected unit and update the Menubutton text."""
        self.selected_unit = unit
        self.unit_selection.config(text=unit)  # Update the button text

    @staticmethod
    def fetch_weather(town):
        url = f"http://api.weatherapi.com/v1/current.json?key=85dbfaf9e0b443378b4142616243112&q={town}&aqi=no"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            messagebox.showerror("Input Error", "Please enter a valid town.")
            return None

    def get_weather(self):
        town = self.entry_for_town.get()

        town_info = self.fetch_weather(town)

        if town_info:
            unit = self.selected_unit.lower()

            degrees = town_info["current"][f"temp_{unit}"]

            messagebox.showinfo(town, f"{degrees}°")


if __name__ == "__main__":
    root = ttk.Window(themename="sandstone")
    weather_app = WeatherApp(root)
    root.mainloop()
