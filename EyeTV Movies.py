import sys
# TODO: Only while developing
sys.path.append("/Users/pnr/Plex-EyeTV-Tools/EyeTV Info/bundle/Contents/Code")

import scanner
import criteria

def Scan(path, files, mediaList, subdirs):
    print "======================Scan...===================="
    print "path  = " + str(path)
    print "files = " + str(files)
    print "media = " + str(mediaList)
    print "subdr = " + str(subdirs)
    scanner.Scan(path, files, mediaList, subdirs, criteria.is_movie)
    print "media = " + str(mediaList)
    print "======================Scan...done================"
