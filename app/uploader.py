# app/uploader.py
import os, threading, mimetypes, json
from datetime import datetime
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from app.encryptor import encrypt_file_stream, secure_delete
from kivy.clock import Clock

DOWNLOAD_DIR = os.path.join('/storage/emulated/0', 'Download')
RESULTS_DIR = os.path.join(DOWNLOAD_DIR, 'AnimeXstreamUploads')
RESULTS_FILE = os.path.join(RESULTS_DIR, 'uploads_log.txt')
VIDEO_EXTS = ('.mp4', '.mkv')

class Uploader:
    def __init__(self, app):
        self.app = app
        self._stop = False
        # attach UI event bindings after UI ready
        Clock.schedule_once(self._attach, 0.1)

    def _attach(self, dt):
        root = self.app.root
        root.ids.rootbox.bind(on_start_upload=lambda *a: self.start(self.app.root.ids.api_key.text.strip(),
                                                                   self.app.root.ids.folder_path.text.strip()))
        root.ids.rootbox.bind(on_stop_upload=lambda *a: self.stop())
        root.ids.rootbox.bind(on_check_update=lambda *a: self.app.updater.check_update_and_prompt())

        # make sure results folder exists
        os.makedirs(RESULTS_DIR, exist_ok=True)

    def start(self, api_key, folder):
        if not api_key or not folder:
            self.app.show_message("API key and folder required")
            return
        self._stop = False
        t = threading.Thread(target=self._worker, args=(api_key, folder), daemon=True)
        t.start()

    def stop(self):
        self._stop = True

    def _find_videos(self, root_dir):
        for dirpath, _, filenames in os.walk(root_dir):
            for fn in filenames:
                if fn.lower().endswith(VIDEO_EXTS):
                    yield os.path.join(dirpath, fn)

    def _upload_file(self, api_key, file_path):
        fname = os.path.basename(file_path)
        enc_path = file_path + ".enc"
        try:
            encrypt_file_stream(file_path, enc_path)
        except Exception as e:
            self._log(f"Encryption failed {fname}: {e}")
            return False, str(e)

        mime_type, _ = mimetypes.guess_type(enc_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        upload_url = f"http://up.abyss.to/{api_key}"

        try:
            with open(enc_path, 'rb') as fh:
                encoder = MultipartEncoder(fields={'file': (os.path.basename(enc_path), fh, mime_type)})
                total = encoder.len
                def monitor_cb(m):
                    frac = m.bytes_read / total if total else 0
                    val = int(min(100, frac*100))
                    Clock.schedule_once(lambda dt: setattr(self.app.root.ids.progress_bar, 'value', val))
                monitor = MultipartEncoderMonitor(encoder, monitor_cb)
                headers = {'Content-Type': monitor.content_type}
                resp = requests.post(upload_url, data=monitor, headers=headers, timeout=3600)
        except Exception as e:
            self._log(f"Upload request error {fname}: {e}")
            try:
                secure_delete(enc_path)
            except Exception: pass
            return False, str(e)

        # remove encrypted temp
        try:
            secure_delete(enc_path)
        except Exception:
            pass

        try:
            data = resp.json()
        except Exception:
            data = {'raw': resp.text}

        if resp.status_code == 200 or data.get('status', True) is True:
            slug = data.get('slug') or data.get('id') or ''
            final_url = f"https://abyss.to/{slug}" if slug else "NO_SLUG"
            # copy to clipboard
            try:
                self.app.copy_to_clipboard(final_url + "  | slug:" + str(slug))
            except Exception:
                pass
            # save to results file
            with open(RESULTS_FILE, 'a', encoding='utf-8') as rf:
                rf.write(f"--- {datetime.now().isoformat()} ---\n")
                rf.write(f"FILE: {file_path}\nSLUG: {slug}\nURL: {final_url}\n\n")
            return True, {'slug': slug, 'url': final_url, 'raw': data}
        else:
            return False, {'status': resp.status_code, 'data': data}

    def _worker(self, api_key, folder):
        files = list(self._find_videos(folder))
        if not files:
            self.app.show_message("No video files (.mp4/.mkv) found.")
            return
        self._log(f"Found {len(files)} files. Starting...")
        for f in files:
            if self._stop:
                self._log("Stopped by user.")
                break
            Clock.schedule_once(lambda dt, p=f: setattr(self.app.root.ids.current_file, 'text', f"Current: {os.path.basename(p)}"))
            ok, res = self._upload_file(api_key, f)
            if ok:
                self._log(f"Uploaded: {os.path.basename(f)} -> {res.get('slug')}")
                # add clickable log entry
                Clock.schedule_once(lambda dt, url=res.get('url'), slug=res.get('slug'): self._add_log_entry(url, slug))
            else:
                self._log(f"Failed: {os.path.basename(f)} -> {res}")
        Clock.schedule_once(lambda dt: setattr(self.app.root.ids.current_file, 'text', "Current: -"))
        Clock.schedule_once(lambda dt: setattr(self.app.root.ids.progress_bar, 'value', 0))
        self.app.show_message("Upload run finished. Results saved to:\n" + RESULTS_FILE)

    def _add_log_entry(self, url, slug):
        la = self.app.root.ids.log_area
        from kivy.uix.label import Label
        lbl = Label(text=f"{slug}  -  {url}", size_hint_y=None, height='30dp')
        # bind touch to play
        def on_touch(instance, touch):
            if instance.collide_point(*touch.pos):
                # open player with URL
                self.app.player.play_url(url)
        lbl.bind(on_touch_down=on_touch)
        la.add_widget(lbl)

    def _log(self, text):
        try:
            la = self.app.root.ids.log_area
            from kivy.uix.label import Label
            lbl = Label(text=text, size_hint_y=None, height='24dp')
            la.add_widget(lbl)
        except Exception:
            print(text)