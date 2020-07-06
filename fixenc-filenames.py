#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import shutil
import sys
import unicodedata

import mutagen

ROOT = "/Users/romansh/private/music"
EXCEPTIONS = ['Wohnout', 'EP Cave n°2']

VERBOSE = True
DRY_RUN = True

def merge_dirs(source, dest):
    files = os.listdir(source)
    for f in files:
        shutil.move(os.path.join(source, f), dest)

    os.rmdir(source)

errors = 0

queue = [ROOT]
ptr = 0

while ptr < len(queue):
    curr = queue[ptr]
    ptr += 1

    if os.path.isdir(curr):
        queue.extend(os.path.join(curr, x) for x in os.listdir(curr))

for path in queue[::-1]:
    if any(dirr in str(path) for dirr in EXCEPTIONS):
        continue

    changed = False
    head, tail = os.path.split(path)

    if all(
        ord(ch) < 0x80 or 0x401 <= ord(ch) < 0x500 or ord(ch) > 0x2000 
            or ord(ch) == 0x306 or ord(ch) == 0x308
        for ch in tail
    ):
        continue

    if VERBOSE:
        print(path)
    try:
        text = tail
        new_text = unicodedata.normalize('NFKC', text).replace(
            ' \u0327', '¸'
        ).encode('cp1252').decode('cp1251')
        new_path = os.path.join(head, new_text)
        if VERBOSE:
            print(path, '→', new_path)
        changed = True

        if not DRY_RUN and changed:
            if os.path.exists(new_path):
                assert os.path.isdir(path) and os.path.isdir(new_path)
                merge_dirs(path, new_path)
            else:
                os.rename(path, new_path)
            #break
        
    except UnicodeEncodeError as e:
        errors += 1
        print(str(e), text)

print("Num errors:", errors)


