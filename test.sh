#!/bin/sh
#

PMS="/OwnApplications/Personal/Plex Media Server.app/"
SCANNER="${PMS}/Contents/MacOS/Plex Media Scanner"
SCANNER_OPTIONS="--verbose --progress"

scan() {
    "${SCANNER}" ${SCANNER_OTIONS} "$@"
}

testit() {
    python setup.py install
    # TODO: The following is silly
    scan --section 6 --scan
}
    
