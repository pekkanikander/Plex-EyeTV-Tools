import sys
# TODO: Only while developing
# sys.path.append("/Users/pnr/Plex-EyeTV-Tools/EyeTV Info/bundle/Contents/Code")

import scanner
import criteria

def Scan(path, files, mediaList, subdirs):
    return scanner.Scan(path, files, mediaList, subdirs, is_series)
