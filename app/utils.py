# app/utils.py
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label

def show_msg_async(app, text):
    def _show(dt):
        p = Popup(title="Info", content=Label(text=text), size_hint=(0.8,0.4))
        p.open()
    Clock.schedule_once(_show, 0)