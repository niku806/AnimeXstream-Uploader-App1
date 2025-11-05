AnimeXstream - Private Uploader (Kivy)

Place this folder on your device. Edit assets/public_key.pem with your server public key.
Add your icon at assets/icon.png.

Build on Termux (mobile) or a Linux PC with Buildozer.

Termux quick deps:
pkg update -y
pkg install python clang zip git wget -y
pip install cython==0.29.36
pip install buildozer
# then run buildozer android debug

Server needs:
- https://gamervip.gt.tc/apk/version.json (with fields version, apk_url, apk_sha256, apk_sig)
- Signed APK uploads.

Important: Silent installs are not allowed; installer will prompt user.