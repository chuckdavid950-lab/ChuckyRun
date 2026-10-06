[app]
title = Chucky Run
package.name = chuckyrun
package.domain = com.chuckyd

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,wav,mp3

version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 1

android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
