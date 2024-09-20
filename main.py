from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from datetime import datetime
import requests
import pytz


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')


        # Logo
        self.logo = Image(source='wee.JPG')
        layout.add_widget(self.logo)


        # Weather Image
        self.weather_image = Image(source='wee.JPG')
        layout.add_widget(self.weather_image)


        # Current Time
        self.time_label = Label(text='')
        layout.add_widget(self.time_label)


        # Set Alarm Button
        self.set_alarm_button = Button(text='Set Alarm')
        self.set_alarm_button.bind(on_press=self.goto_alarm_screen)
        layout.add_widget(self.set_alarm_button)


        self.add_widget(layout)
        Clock.schedule_interval(self.update_time_and_weather, 60)  # Update every minute


    def goto_alarm_screen(self, instance):
        self.manager.current = 'alarm'


    def update_time_and_weather(self, *args):
        # Update Time
        now = datetime.now(pytz.timezone('Asia/Kathmandu'))
        self.time_label.text = now.strftime('%Y-%m-%d %H:%M:%S')


        # Update Weather Image
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Kathmandu&appid=your_api_key')
        weather = response.json()
        weather_condition = weather['weather'][0]['main'].lower()
        self.weather_image.source = f'{weather_condition}.JPG'


class AlarmScreen(Screen):
    def __init__(self, **kwargs):
        super(AlarmScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)


        # Set Alarm Time using Spinners
        self.hour_spinner = Spinner(text='Hour', values=[f'{i:02d}' for i in range(24)])
        self.minute_spinner = Spinner(text='Minute', values=[f'{i:02d}' for i in range(60)])
        layout.add_widget(self.hour_spinner)
        layout.add_widget(self.minute_spinner)


        # Weather Condition Selector
        self.weather_condition_input = TextInput(hint_text='Enter weather condition', multiline=False)
        layout.add_widget(self.weather_condition_input)


        # Alarm Condition Switch
        self.weather_condition_switch = Switch(active=True)
        self.weather_condition_label = Label(text='Ring the alarm if weather condition matches')
        layout.add_widget(self.weather_condition_switch)
        layout.add_widget(self.weather_condition_label)


        # Save Button
        self.save_button = Button(text='Save Alarm')
        self.save_button.bind(on_press=self.save_alarm)
        layout.add_widget(self.save_button)


        self.add_widget(layout)


    def save_alarm(self, instance):
        alarm_hour = self.hour_spinner.text
        alarm_minute = self.minute_spinner.text
        weather_condition = self.weather_condition_input.text
        # Logic to save the alarm settings (you can implement the saving logic here)
        print(f'Alarm set for {alarm_hour}:{alarm_minute} with weather condition {weather_condition}')


class AlarmApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AlarmScreen(name='alarm'))
        return sm


if __name__ == '__main__':
    AlarmApp().run()



