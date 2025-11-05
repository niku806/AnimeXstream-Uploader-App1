[app]
title = AnimeXstream - Private Uploader
package.name = animexstream
package.domain = org.animexstream
source.dir = .
source.include_exts = py,kv,png,jpg,pem,txt
version = 0.1.0
requirements = python3,kivy==2.1.0,pyjnius,requests,requests-toolbelt,pycryptodome,plyer,tqdm
orientation = portrait
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,REQUEST_INSTALL_PACKAGES
android.api = 33
android.minapi = 21
icon.filename = assets/icon.png
# If you plan to request MANAGE_EXTERNAL_STORAGE uncomment below (note Play Store rules)
# android.permissions += MANAGE_EXTERNAL_STORAGE
# Add these lines if you will merge manifest/provider (see README)
# android.add_default_android_manifest = True