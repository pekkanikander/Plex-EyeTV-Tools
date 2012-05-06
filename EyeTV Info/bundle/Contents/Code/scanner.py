import re, os, os.path, sys
import Media, UnicodeHelper, unicodedata, plistlib

class Scanner(object):

    suffix     = ".eyetv"
    liveSuffix = "Live TV Buffer.eyetv"

    def __init__(self, type='Movie'):
        self.type = type

    def Scan(self, path, files, mediaList, subdirs):
        recording = None
        if len(files) < 1:
            return
        if path.endswith(self.suffix) and not path.endswith(self.liveSuffix):
            recording = self.FindRecording(path, files)
        if recording:
            movie = Media.Movie(path.split('/')[-1])
            movie.parts.append(recording)
            mediaList.append(movie)

    def FindRecording(self, path, files):
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
                if (genre == "!Movie" or 
                    (genre == "!Children" and duration > 50 * 60) or
                    (genre == "!Documentary" and duration > 50 * 60)):
                    OkRecording = True

        return recording if OkRecording else None
                        
