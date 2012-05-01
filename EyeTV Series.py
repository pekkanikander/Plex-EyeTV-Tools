import re, os, os.path, sys
import Media, UnicodeHelper, unicodedata, plistlib

def Scan(path, files, mediaList, subdirs):
    if len(files) >= 1:
        if path.endswith(".eyetv") and not path.endswith("Live TV Buffer.eyetv"):
            OkRecording = None
            recording = None
            genre = None
            duration = 0
            for file in files:
                if file.endswith(".mpg"):
                    recording = file
                if file.endswith(".eyetvp"):
                    pl = plistlib.readPlist(file)
                    try: genre = pl['epg info']['VIDEO']
                    except: pass
                    try: duration = pl['epg info']['DURATION']
                    except: pass
                    if (genre != "!Movie" and
                        (genre != "!Children" or duration <= 50 * 60) and
                        (genre != "!Documentary" or duration <= 50 * 60)):
                        OkRecording = True
                        
            if OkRecording and recording:
                movie = Media.Movie(path.split('/')[-1])
                movie.parts.append(recording)
                mediaList.append(movie)
