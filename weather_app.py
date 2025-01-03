import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from ttkbootstrap.window import Toplevel


class WeatherApp:
    def __init__(self, master) -> None:
        self.master = master
        self.master.geometry("400x350")
        self.master.title("Weather App")

        # Configure columns for responsiveness
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)

        # Title Label
        ttk.Label(self.master, text="Weather App", font=("Helvetica", 20), bootstyle=INFO).grid(row=0, column=1, pady=20)

        # Entry Label
        ttk.Label(self.master, text="Enter a town:", font=("Helvetica", 15)).grid(row=1, column=1, pady=10)

        # Entry Field
        self.entry_for_town = ttk.Entry(self.master, bootstyle=PRIMARY, width=30)
        self.entry_for_town.grid(row=2, column=1, padx=10, pady=10)

        # Clear Button
        self.clear_button = ttk.Button(
            self.master,
            text="Clear",
            command=self.clear_entry,
            bootstyle="outline"
        )
        self.clear_button.grid(row=3, column=1, padx=10, pady=10)

        # Menubutton for selecting temperature unit
        self.unit_selection = ttk.Menubutton(self.master, text="C / F", bootstyle=PRIMARY)
        self.unit_selection.grid(row=4, column=1, padx=10, pady=10)

        # Create a menu and associate it with the Menubutton
        self.unit_menu = ttk.Menu(self.unit_selection, tearoff=0)
        self.unit_selection["menu"] = self.unit_menu

        self.unit_menu.add_command(label="Celsius (C)", command=lambda: self.set_unit("C"))
        self.unit_menu.add_command(label="Fahrenheit (F)", command=lambda: self.set_unit("F"))

        self.selected_unit = "C"

        # Show Weather Button
        self.button_to_show_weather = ttk.Button(self.master, text="Show Weather", command=self.get_weather)
        self.button_to_show_weather.grid(row=5, column=1, pady=20)

    def clear_entry(self):
        """Clear the town entry field."""
        self.entry_for_town.delete(0, 'end')

    def set_unit(self, unit):
        """Set the selected unit and update the Menubutton text."""
        self.selected_unit = unit
        self.unit_selection.config(text=unit)  # Update the button text

    @staticmethod
    def fetch_weather(url):
        """Fetch weather data from the API."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to fetch weather data. Please check your internet connection or API key.")
            return None

    def aqi_for_town(self, town_aqi, town_name):
        window_aqi = Toplevel()
        window_aqi.geometry("400x300")
        window_aqi.title(f"Air quality index: {town_name}:")

        ttk.Label(window_aqi, text=f"Air quality index(aqi) of {town_name}",
                  font=("Helvetica", 20), bootstyle=INFO).pack(pady=10)

        for element, quality in town_aqi.items():
            ttk.Label(window_aqi, text=f"{element}: {quality}", font=("Helvetica", 15)).pack(pady=5)

    def weather_of_town(self, town_info, town_name: str):
        """Display the weather of the entered town in a new window."""
        town_window = Toplevel()
        town_window.geometry("400x280")
        town_window.title(f"Weather: {town_name}")

        unit = self.selected_unit.lower()
        current_weather = town_info["current"]

        # Extract weather details
        degrees = current_weather[f"temp_{unit}"]
        feels_like = current_weather[f"feelslike_{unit}"]
        condition = current_weather["condition"]["text"]
        humidity = current_weather["humidity"]
        wind_speed = current_weather["wind_kph"]

        # Display Weather Details
        ttk.Label(town_window, text=f"Weather in {town_name}:", font=("Helvetica", 20), bootstyle=INFO).pack(pady=10)
        ttk.Label(town_window, text=f"Temperature: {degrees}°", font=("Helvetica", 15)).pack(pady=5)
        ttk.Label(town_window, text=f"Feels Like: {feels_like}°", font=("Helvetica", 15)).pack(pady=5)
        ttk.Label(town_window, text=f"Condition: {condition}", font=("Helvetica", 15)).pack(pady=5)
        ttk.Label(town_window, text=f"Humidity: {humidity}%", font=("Helvetica", 15)).pack(pady=5)
        ttk.Label(town_window, text=f"Wind Speed: {wind_speed} kph", font=("Helvetica", 15)).pack(pady=5)

        aqi = current_weather["air_quality"]

        button_aqi = ttk.Button(town_window, text="See air quality index(aqi)",
                                command=lambda: self.aqi_for_town(aqi, town_name))
        button_aqi.pack(pady=10)

        town_window.mainloop()

    def get_weather(self):
        """Fetch weather data and display it."""
        town = self.entry_for_town.get().strip()
        if not town:
            messagebox.showwarning("Input Error", "Please enter a valid town name.")
            return

        url = f"http://api.weatherapi.com/v1/current.json?key=85dbfaf9e0b443378b4142616243112&q={town}&aqi=yes"

        town_info = self.fetch_weather(url)

        if town_info:
            self.weather_of_town(town_info, town)


if __name__ == "__main__":
    root = ttk.Window(themename="sandstone")
    weather_app = WeatherApp(root)
    root.mainloop()
