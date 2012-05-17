import Media, plistlib

recdSuffix  = ".eyetv"
metaSuffix  = ".eyetvp"
liveSuffix  = "Live TV Buffer.eyetv"
videoSuffix = ".mpg"  # Use .m4v if you needed

def Scan(path, files, mediaList, subdirs, isOfGenre):
    """Scans the path for an EyeTV recording of the given genre.
    
    An EyeTV recording consists of the actual video file(s) and a set
    of metadata files.  First makes sure that the given files do exist.
    Then inspect the metadata to see if the recording belongs to the
    desired genre.

    isOfGenre is a function that takes a plist as its argument.
    
    """

    if len(files) < 1:
        return
    if path.endswith(recdSuffix) and not path.endswith(liveSuffix):
        recording = FindRecording(files, isOfGenre)
        if recording:
            movie = Media.Movie(path.split('/')[-1]) # Last part of the path
            movie.parts.append(recording)
            mediaList.append(movie)

def FindRecording(files, isOfGenre):
    """Attempts to locate a recording of the given genre among files.

    Scan for a video file and metadata file, and then apply isOfGenre
    on the plist read from the metadata file.
    """
    recording = None
    metadata  = None

    for file in files:
        if file.endswith(videoSuffix):
            recording = file
        if file.endswith(metaSuffix):
            metadata  = file
        if recording and metadata:
            if isOfGenre(plistlib.readPlist(metadata)):
                return recording

    return None
                        
