#!/usr/bin/python
# -*- coding: utf-8 -*-

import re


def lookupPlist(plist, *args):
    for key in args:
        try:
            plist = plist[key]
        except KeyError:
            return None
    return plist

def is_movie1(genre, duration):
    return ((genre == "!Movie" and duration > 61 * 60) or 
            (genre == "!Children" and duration > 59 * 60) or
            (genre == "!Documentary" and duration > 61 * 60))

def is_movie(plist):
    genre    = lookupPlist(plist, 'epg info', 'VIDEO')
    duration = lookupPlist(plist, 'epg info', 'DURATION')
    return is_movie1(genre, duration)

def is_series(plist):
    genre    = lookupPlist(plist, 'epg info', 'VIDEO')
    duration = lookupPlist(plist, 'epg info', 'DURATION')
    return genre != None and not is_movie1(genre, duration)

# 
# TODO: Make into preferences
#

# Each line is a tuple ( criteria, collection )
# Each criteria is a list of tuples ( key, regexp )
# The criteria match if all keys exist and and the regexp match the values found
# 
collectionPatterns = [
    ( [('TITLE',    '^Andersenin satuja'),  ('VIDEO', '!Children'   )], 'Andersenin satuja'  ),
    ( [('TITLE',    '^Anna ystävämme'),     ('VIDEO', '!Children'   )], 'Anna ystävämme'     ),
    ( [('TITLE',    '^Anne Frankin päivä'), ('VIDEO', '!Movie'      )], 'Anne Frankin päiväkirja' ),
    ( [('TITLE',    '^Anniina Ballerina'),  ('VIDEO', '!Children'   )], 'Anniina Ballerina'  ),
    ( [('TITLE',    '^Avara luonto'),       ('VIDEO', '!Documentary')], 'Avara luonto'       ),
    ( [('TITLE',    '^Barbie[: ]'),         ('VIDEO', '!Children'   )], 'Barbie'             ),
    ( [('TITLE',    '^Barbie[: ]'),         ('VIDEO', '!Movie'      )], 'Barbie'             ),
    ( [('TITLE',    '^.*Barbie esittää:'),  ('VIDEO', '!Movie'      )], 'Barbie'             ),
    ( [('ABSTRACT', '^Barbie[: ]'),         ('VIDEO', '!Children'   )], 'Barbie'             ),
    ( [('TITLE',    '^Daltonit'),           ('VIDEO', '!Children'   )], 'Daltonit'           ),
    ( [('TITLE',    '^Dinojuna'),           ('VIDEO', '!Children'   )], 'Dinojuna'           ),
    ( [('TITLE',    '^Emilien tytär'),      ('VIDEO', '!Movie'      )], 'Emilien tytär'      ),
    ( [('TITLE',    '.*Huippumalli haussa'),('VIDEO', '!Movie'      )], 'Huippumalli haussa' ),
    ( [('TITLE',    '^H. C. Andersen:'),    ('VIDEO', '!Children'   )], 'Andersenin satuja'  ),
    ( [('TITLE',    '^H.C.Andersen:'),      ('VIDEO', '!Children'   )], 'Andersenin satuja'  ),
    ( [('TITLE',    '^H.C.Andersenin'),     ('VIDEO', '!Children'   )], 'Andersenin satuja'  ),
    ( [('TITLE',    '^H2O'),                ('VIDEO', '!Movie'      )], 'H2O'                ),
    ( [('TITLE',    '^Hillitön hotelli'),   ('VIDEO', '!Children'   )], 'Hillitön hotelli'   ),
    ( [('TITLE',    '^Hirveä Henri'),       ('VIDEO', '!Children'   )], 'Hirveä Henri'       ),
    ( [('TITLE',    '^Hirviöallergiaa'),    ('VIDEO', '!Children'   )], 'Hirviöallergiaa'    ),
    ( [('TITLE',    '^Idols'),              ('VIDEO', '!Music'      )], 'Idols'              ),
    ( [('TITLE',    '^Kaapo'),              ('VIDEO', '!Children'   )], 'Kaapo'              ),
    ( [('TITLE',    '^Karhulan nukkesaira'),('VIDEO', '!Children'   )], 'Karhulan nukkesairaala' ),
    ( [('TITLE',    '^Karhuset'),           ('VIDEO', '!Children'   )], 'Karhuset'           ),
    ( [('TITLE',    '^Karvinen'),           ('VIDEO', '!Children'   )], 'Karvinen'           ),
    ( [('TITLE',    '^Lapsityrannit'),      ('VIDEO', '!Documentary')], 'Lapsityrannit'      ),
    ( [('TITLE',    '^Lauri kilpa-auto:'),  ('VIDEO', '!Children'   )], 'Lauri kilpa-auto'   ),
    ( [('TITLE',    '^Lego Ninjago'),       ('VIDEO', '!Children'   )], 'Lego Ninjago'       ),
    ( [('TITLE',    '^Madagascarin pingvi'),('VIDEO', '!Children'   )], 'Madagascarin pingviinit' ),
    ( [('TITLE',    '^Muumi ja vaara'),     ('VIDEO', '!Movie'      )], 'Muumi'              ),
    ( [('TITLE',    '^Muumilaakson tarino'),('VIDEO', '!Children'   )], 'Muumi'              ),
    ( [('TITLE',    '^Muumipeikko'),        ('VIDEO', '!Movie'      )], 'Muumi'              ),
    ( [('TITLE',    '^Palomies Sami'),      ('VIDEO', '!Children'   )], 'Palomies Sami'      ),
    ( [('TITLE',    '^Peppi Pitkätossu'),   ('VIDEO', '!Children'   )], 'Peppi Pitkätossu'   ),
    ( [('TITLE',    '^Pieni runotyttö'),    ('VIDEO', '!Movie'      )], 'Pieni runotyttö'    ),
    ( [('TITLE',    '^Pikku kakkonen'),     ('VIDEO', '!Children'   )], 'Pikku kakkonen'     ),
    ( [('TITLE',    '^Ruohonjuuritasolla'), ('VIDEO', '!Children'   )], 'Ruohonjuuritasolla' ),
    ( [('TITLE',    '^Smurffit'),           ('VIDEO', '!Children'   )], 'Smurffit'           ),
    ( [('TITLE',    '^Taotao, pieni panda'),('VIDEO', '!Children'   )], 'Taotao'             ),
    ( [('TITLE',    '^TV2: H.C.Andersen:'), ('VIDEO', '!Children'   )], 'Andersenin satuja'  ),
    ( [('TITLE',    '^TV2: H2O'),           ('VIDEO', '!Movie'      )], 'H2O'                ),
    ( [('TITLE',    '^TV2: Hillitön hotel'),('VIDEO', '!Children'   )], 'Hillitön hotelli'   ),
    ( [                                     ('VIDEO', '!Children'   )], 'Lasten'             ),
    ]

def collections(plistp, plistr):
    collections = []
    info = lookupPlist(plistp, 'epg info')
    if not info:
        return None
    for (pattern, collection) in collectionPatterns:
        match = True
        for (key, regexp) in pattern:
            value = lookupPlist(info, key)
            if not value or not re.match(regexp, value): 
                match = False
        if match:
            collections.append(collection)

    return collections

def tags(plistp, plistr):
    pass

# 
# Unit tests -- very much work in progress
#
if __name__ == "__main__":
    # Test lookupPlist
    pl = dict(
        aDict=dict(
            anotherString="<hello & hi there!>",
            aUnicodeValue=u'M\xe4ssig, Ma\xdf',
            aTrueValue=True,
            aFalseValue=False,
        ),
    )
    assert lookupPlist(pl, 'aDict', 'aTrueValue')    == True
    assert lookupPlist(pl, 'aDict', 'aMissingValue') == None

    # Test is_movie1
    assert is_movie1("!Movie", 3661)
    assert is_movie1("!Children", 3541)
    assert is_movie1("!Documentary", 3661)
    assert not is_movie1("!Children", 1800)
    assert not is_movie1("!Documentary", 1800)
    assert not is_movie1("!Series", 0)

    # Test is_movie and is_series
    movie1 = { 'epg info' : { 'VIDEO' : '!Movie',       'DURATION' : 3661, 'TITLE' : 'Barbie ' }}
    movie2 = { 'epg info' : { 'VIDEO' : '!Children',    'DURATION' : 3661, 'TITLE' : 'Barbie:' }}
    movie3 = { 'epg info' : { 'VIDEO' : '!Documentary', 'DURATION' : 3661, 'TITLE' : 'Avara luonto: ' }}
    serie1 = { 'epg info' : { 'VIDEO' : '!Series',      'DURATION' : 0,    'TITLE' : 'Prisma: ' }}
    serie2 = { 'epg info' : { 'VIDEO' : '!Children',    'DURATION' : 1800, 'TITLE' : 'Pikku kakkonen: ' }}
    serie3 = { 'epg info' : { 'VIDEO' : '!Documentary', 'DURATION' : 1800, 'TITLE' : '' }}
    assert is_movie(movie1)
    assert is_movie(movie2)
    assert is_movie(movie3)
    assert is_series(serie1)
    assert is_series(serie2)
    assert is_series(serie3)

    # Test collections
    assert collections(movie1, None) == ['Barbie']
    assert collections(movie2, None) == ['Barbie', 'Lasten']
    assert collections(movie3, None) == ['Avara luonto']
