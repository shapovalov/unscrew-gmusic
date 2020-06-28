#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import unicodedata

import mutagen

ROOT = "/Users/romansh/private/music"
EXCEPTIONS = ['Wohnout']

VERBOSE = False
DRY_RUN = True

KEYS = ['TIT2', 'TPE1', 'TALB']

errors = 0

for path in Path(ROOT).rglob('*.mp3'):
    if any(dirr in str(path.absolute()) for dirr in EXCEPTIONS):
        continue

    f = mutagen.File(path)
    changed = False
    for key in KEYS:
        if key not in f or all(
            ord(ch) < 0x80 or 0x401 <= ord(ch) < 0x500 or ord(ch) > 0x2000
            for ch in f[key].text[0]
        ):
            continue

        if VERBOSE:
            print(path)
        try:
            text = f[key].text[0]
            new_text = unicodedata.normalize('NFKC', text).replace(
                ' \u0327', '¸'
            ).encode('cp1252').decode('cp1251')
            if VERBOSE:
                print(text, '→', new_text)
            changed = True
            f[key].text[0] = new_text
        except UnicodeEncodeError as e:
            errors += 1
            print(str(e), text)

    if not DRY_RUN and changed:
        f.save()
        #break

print("Num errors:", errors)


