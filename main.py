# main.py
import os, json
from kivy.app import App
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from app.encryptor import ensure_key
from app.uploader import Uploader
from app.updater import Updater
from app.player import PlayerScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

KV = Builder.load_file(os.path.join('app', 'ui.kv'))

class RootBox(BoxLayout):
    pass

class AnimeXApp(App):
    def build(self):
        self.title = "AnimeXstream - Private Uploader"
        ensure_key()
        # instantiate modules (they attach to UI later)
        self.uploader = Uploader(app=self)
        self.updater = Updater(app=self, update_base_url="https://gamervip.gt.tc/apk")
        self.player = PlayerScreen(app=self)
        root = KV
        # attach custom events for the root box
        root.ids.rootbox.bind(on_pick_saf=self._pick_saf,
                              on_pick_simple=self._pick_simple,
                              on_start_upload=self._start_upload,
                              on_stop_upload=self._stop_upload,
                              on_check_update=self._check_update,
                              on_open_player=self._open_player)
        # load saved config
        self.cfg_path = os.path.join(self.user_data_dir, 'config.json')
        self._load_config()
        return root

    def _load_config(self):
        try:
            if os.path.exists(self.cfg_path):
                with open(self.cfg_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.root.ids.api_key.text = data.get('api_key','')
                    self.root.ids.folder_path.text = data.get('folder_path','')
        except Exception as e:
            print("Config load error:", e)

    def save_config(self):
        try:
            data = {'api_key': self.root.ids.api_key.text.strip(),
                    'folder_path': self.root.ids.folder_path.text.strip()}
            os.makedirs(os.path.dirname(self.cfg_path), exist_ok=True)
            with open(self.cfg_path, 'w', encoding='utf-8') as f:
                json.dump(data, f)
            self.show_message("Config saved.")
        except Exception as e:
            self.show_message("Save failed: " + str(e))

    def _pick_simple(self, *a):
        # user types path manually; we only hint
        self.show_message("Type the folder path in the Folder field and press Save, or use SAF picker.")

    def _pick_saf(self, *a):
        # attempt SAF via pyjnius (Android only)
        try:
            from app.keystore import pick_directory_saf
            pick_directory_saf(self)
        except Exception as e:
            self.show_message("SAF not available: " + str(e))

    def _start_upload(self, *a):
        api = self.root.ids.api_key.text.strip()
        folder = self.root.ids.folder_path.text.strip()
        if not api:
            self.show_message("API Key required.")
            return
        if not folder:
            self.show_message("Folder path required (or use SAF picker).")
            return
        # start uploader
        self.uploader.start(api, folder)

    def _stop_upload(self, *a):
        self.uploader.stop()

    def _check_update(self, *a):
        self.updater.check_update_and_prompt()

    def _open_player(self, *a):
        # open a small floating player screen (popup) where user can paste URL or tap log entries
        self.player.open_player_popup()

    def copy_to_clipboard(self, text):
        try:
            Clipboard.copy(text)
            return True
        except Exception as e:
            print("Clipboard failed:", e)
            return False

    def show_message(self, txt):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        p = Popup(title='Info', content=Label(text=txt), size_hint=(0.8,0.4))
        p.open()

if __name__ == '__main__':
    AnimeXApp().run()