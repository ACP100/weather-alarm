from kivy.app import App
from kivy.uix.screenmanager import ScreenManager , Screen
from kivy.clock import Clock
from kivy.uix.image import Image
from kivymd.uix.pickers import MDTimePicker
from datetime import datetime
import requests
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.go_to_home, 3)

    def go_to_home(self, *args):
        self.manager.current = 'home'
    
class HomeScreen(Screen):
    def update_time(self, *args):
        self.ids.time_label.text = datetime.now().strftime("%H:%M:%S")
    
    def on_center(self):
        Clock.schedule_interval(self.update_time, 1)

class AlarmSettinngScreen(Screen):
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_alarm_time)
        time_dialog.open()
    
    def get_alarm_time(self, instance, time):
        self.ids.alarm_time.text = str(time)
    
class WeatherAlarmApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AlarmSettinngScreen(name='alarm_setting'))
        return sm
    
if __name__ == 'main':
    WeatherAlarmApp().run()
