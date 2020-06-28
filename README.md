# Unscrew Google Music
Fix the encoding for Cyrillic tags screwed up by Google Music

Background. I had upploaded mp3 files to Google Music in the dark time when Unicode was not given for granted. Some of the tags had correct encoding labels (cp1251), and some were missing. Google Music converted everything to UTF-16 assuming Latin-1 encoding where unknown, so now it is difficult to fix.

Usage. If you use it for Google Music, install the Music Manager app and download the collection. This script implements some heuristics that distinguish correctly converted Cyrillic names against the faulty ones, and fixes the latter. The cases of genuine Latin-1 encoding (e.g. Czech) have to be manually found and added to `EXCEPTIONS`. For that, the script can be run with `DRY_RUN=True; VERBOSE=True`, then both switched to `False` for the proper conversion.
