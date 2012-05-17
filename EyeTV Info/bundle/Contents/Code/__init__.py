import datetime, time, os, re, os.path, glob, plistlib, unicodedata, hashlib, urlparse, types, urllib

import criteria

class eyetvinfo(Agent.Movies):
    name = 'EyeTV File Info'
    primary_provider = True
    languages = [Locale.Language.English]
        
    def search(self, results, media, lang):
        filename = media.items[0].parts[0].file.decode('utf-8')
        id = media.items[0].parts[0].id
        mod_time = os.path.getmtime(filename)
                
        results.Append(MetadataSearchResult(id=id, name=media.name, 
                                            year=time.localtime(mod_time)[0], lang=lang, score=100))
                
    def update(self, metadata, media, lang):
        filename = media.items[0].parts[0].file.decode('utf-8')
        mod_time = os.path.getmtime(filename)
        date = datetime.date.fromtimestamp(mod_time)
        metadata.year = int(date.year)
        metadata.originally_available_at = Datetime.ParseDate(str(date)).date()
        path = os.path.dirname(filename)

        for pfile in glob.glob1(path, '*.eyetvr'):
            Log("R: " + pfile)
        plistr = plistlib.readPlist(path + "/" + pfile)

        for pfile in glob.glob1(path, '*.eyetvp'):
            Log("P: " + pfile)
        plistp = plistlib.readPlist(path + "/" + pfile)

        thumbnail = None
        # Doesn't seem to work with tiff...
        #for tfile in glob.glob1(path, '*.thumbnail.tiff'):
        #    Log("T: " + tfile)
        #    thumbnail = path + '/' + tfile

        # Movie year from eyetvp, if available
        year = plistp['epg info']['YEAR']
        metadata.year = year if year else metadata.year

        # Recording Name
        try: metadata.title = plistr['info']['recording title'].encode('utf-8')
        except: pass

        # Recording Tag Line
        try: metadata.tagline = str(date) + ':  ' + str(plistr['display title'].encode('utf-8'))
        except: pass

        # Recording Description
        try: metadata.summary = plistr['info']['description'].encode('utf-8')
        except: pass

        if not metadata.summary:
            try: metadata.summary = plistp['epg info']['ABSTRACT']
            except: pass

        # Recording Studio / channel name (TODO: Something saner here?)
        try: metadata.studio = plistr['channel name'].encode('utf-8')
        except: pass

        # Recording Duration
        try: metadata.duration = int(plistr['info']['duration']) * 1000
        except: pass

        # Poster
        if thumbnail:
            if thumbnail not in metadata.posters:
                metadata.posters[thumbnail] = Proxy.Media(Core.storage.load(thumbnail))

        # Genre
        try:
            genre = plistp['epg info']['CONTENT']
            if genre:
                metadata.genres = [genre]
        except: pass

        # Writers
        
        # Directors -- avoid set of one empty string
        try: 
            director = plistp['epg info']['DIRECTOR']
            if director:
                metadata.directors = [director]
        except: pass

        # Collections
        metadata.collections = criteria.collections(plistp, plistr)

        # Tags
        # TBD
