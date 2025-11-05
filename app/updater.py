# app/updater.py
import os, requests, tempfile, hashlib, base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

try:
    from jnius import autoclass
    ANDROID = True
except Exception:
    ANDROID = False

class Updater:
    def __init__(self, app, update_base_url):
        self.app = app
        self.base = update_base_url.rstrip('/')
        pubp = os.path.join('assets', 'public_key.pem')
        if os.path.exists(pubp):
            with open(pubp, 'r', encoding='utf-8') as f:
                self.public_pem = f.read()
        else:
            self.public_pem = None

    def check_update_and_prompt(self):
        try:
            url = f"{self.base}/version.json"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            self.app.show_message("Update check failed: " + str(e))
            return
        latest = data.get('version')
        if not latest:
            self.app.show_message("Invalid version.json")
            return
        current = "0.1.0"
        if latest == current:
            self.app.show_message("App up to date.")
            return
        apk_url = data.get('apk_url')
        apk_sha = data.get('apk_sha256')
        apk_sig = data.get('apk_sig')
        if not apk_url or not apk_sha or not apk_sig or not self.public_pem:
            self.app.show_message("Update metadata incomplete.")
            return
        try:
            self.app.show_message("Downloading update...")
            apk_path = self.download_and_verify(apk_url, apk_sha, apk_sig)
        except Exception as e:
            self.app.show_message("Download/verify failed: " + str(e))
            return
        if ANDROID:
            self.install_apk(apk_path)
        else:
            self.app.show_message("Downloaded APK at: " + apk_path)

    def download_and_verify(self, apk_url, expected_sha, sig_b64):
        r = requests.get(apk_url, stream=True, timeout=60)
        r.raise_for_status()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.apk')
        sha = hashlib.sha256()
        for chunk in r.iter_content(1024*1024):
            if not chunk: break
            tmp.write(chunk)
            sha.update(chunk)
        tmp.close()
        shahex = sha.hexdigest()
        if shahex != expected_sha:
            os.remove(tmp.name)
            raise Exception("SHA mismatch")
        pub = RSA.import_key(self.public_pem)
        sig = base64.b64decode(sig_b64)
        hobj = SHA256.new(sha.digest())
        try:
            pkcs1_15.new(pub).verify(hobj, sig)
        except Exception as e:
            os.remove(tmp.name)
            raise Exception("Signature verify failed: " + str(e))
        return tmp.name

    def install_apk(self, apk_path):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            File = autoclass('java.io.File')
            FileProvider = autoclass('androidx.core.content.FileProvider')

            activity = PythonActivity.mActivity
            file = File(apk_path)
            authority = activity.getPackageName() + ".fileprovider"
            contentUri = FileProvider.getUriForFile(activity, authority, file)

            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(contentUri, "application/vnd.android.package-archive")
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            activity.startActivity(intent)
        except Exception as e:
            self.app.show_message("Install intent failed: " + str(e))