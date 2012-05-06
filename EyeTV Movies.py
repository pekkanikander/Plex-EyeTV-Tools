from scanner import Scanner

def Scan(path, files, mediaList, subdirs):
    scanner = Scanner('Movie')
    return scanner.Scan(path, files, mediaList, subdirs)
