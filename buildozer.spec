[app]
title = Antibio SFAR
package.name = antibiosfar
package.domain = org.sfar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
# Liste stricte des requirements
requirements = python3,kivy==2.2.1,kivymd==1.1.1,sdl2_ttf==2.0.15,pillow,openssl

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.private_storage = True
android.accept_sdk_license = True
android.entrypoint = org.kivy.android.PythonActivity
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1