# app/keystore.py
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

USER_KEY_FILE = os.path.join(os.path.expanduser("~"), ".animexstream_key")

def is_android():
    try:
        import jnius
        return True
    except Exception:
        return False

def pick_directory_saf(app):
    """
    Launches ACTION_OPEN_DOCUMENT_TREE to pick a directory and stores its URI in app config.
    Requires pyjnius.
    """
    try:
        from jnius import autoclass, cast
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        activity = PythonActivity.mActivity
        Intent = autoclass('android.content.Intent')
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)
        REQUEST_CODE = 9999
        activity.startActivityForResult(intent, REQUEST_CODE)
        app.show_message("SAF picker opened. After choosing folder, paste the returned URI into Folder field.")
    except Exception as e:
        app.show_message("SAF pick failed: " + str(e))

# Keystore advanced functions are complex: implement later if you need full wrap/unwrap
# For now, rely on file key. If you need the Keystore implementation (wrap AES using RSA keystore),
# tell me and I'll provide the full pyjnius sample (long).