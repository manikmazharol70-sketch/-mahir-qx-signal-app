[app]

title = MaHiR QX Signal App
package.name = mahirqxsignal
package.domain = org.mahirqx

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

# Android settings
android.api = 35
android.minapi = 21
android.archs = arm64-v8a

# App icon (optional)
# icon.filename = %(source.dir)s/icon.png

[buildozer]

log_level = 2
warn_on_root = 1
