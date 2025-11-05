# app/player.py
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import os

class PlayerScreen:
    def __init__(self, app):
        self.app = app
        self.popup = None
        self.video = None

    def open_player_popup(self):
        if self.popup and self.popup._window:
            self.popup.dismiss()
        box = BoxLayout(orientation='vertical', spacing=6, padding=6)
        self.video = Video(source='', state='stop')
        self.video.options = {'eos': 'stop'}
        box.add_widget(self.video)

        control = BoxLayout(size_hint_y=None, height='40dp', spacing=6)
        self.input = TextInput(hint_text='Paste URL or local path here', multiline=False)
        btn_play = Button(text='Play', size_hint_x=None, width='80dp')
        btn_stop = Button(text='Stop', size_hint_x=None, width='80dp')
        control.add_widget(self.input)
        control.add_widget(btn_play)
        control.add_widget(btn_stop)
        box.add_widget(control)

        def on_play(instance):
            src = self.input.text.strip()
            if not src:
                self.app.show_message("Enter URL or local path")
                return
            # if it's a local file and exists, use that
            if os.path.exists(src):
                self.video.source = src
            else:
                self.video.source = src
            self.video.state = 'play'
        def on_stop(instance):
            if self.video:
                self.video.state = 'stop'

        btn_play.bind(on_release=on_play)
        btn_stop.bind(on_release=on_stop)

        self.popup = Popup(title='Video Player', content=box, size_hint=(0.95,0.95))
        self.popup.open()

    def play_url(self, url):
        # open popup and play
        self.open_player_popup()
        Clock.schedule_once(lambda dt: setattr(self.input, 'text', url), 0.1)
        Clock.schedule_once(lambda dt: self.video._reload(), 0.3)
        Clock.schedule_once(lambda dt: setattr(self.video, 'state', 'play'), 0.4)