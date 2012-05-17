#!/bin/sh
#

PMS="/OwnApplications/Personal/Plex Media Server.app/"
SCANNER="${PMS}/Contents/MacOS/Plex Media Scanner"
SCANNER_OPTIONS="--verbose --progress"

scan() {
    "${SCANNER}" ${SCANNER_OTIONS} "$@"
}

renew-files() {
    for i in test-data/*/*; do touch "$i"; done
    A_SIZE=`du video-samples/SampleA.mpg | cut -f1`
    B_SIZE=`du video-samples/SampleB.mpg | cut -f1`
    for i in test-data/*; do
        SIZE=`du "$i"/*.mpg 2>/dev/null | cut -f1`
        rm -f "$i"/*.mpg
        if [ $SIZE -eq $A_SIZE ] 2>/dev/null; then
            cp video-samples/SampleB.mpg "$i"
        else
            cp video-samples/SampleA.mpg "$i"
        fi
    done
}

testit() {
    python setup.py install
    tail -q -F "$HOME/Library/Logs/Plex Media Scanner.log" | cut -c1-160 &
    TAIL1="$!"
    tail -q -F "$HOME/Library/Logs/PMS Plugin Logs/com.plexapp.system.log" | 
          cut -c1-160 &
    TAIL2="$!"
    tail -q -F "$HOME/Library/Logs/PMS Plugin Logs/fi.iki.pnr.plex.agents.eyetv_info.log" | 
          cut -c1-160 &
    TAIL3="$!"
    sleep 1
    # TODO: The following is silly
    echo "=======================STARTING3========================================="
    scan --section 6 --force --scan
    sleep 1
    echo "=======================ENDING3==========================================="
    killall tail
}
    
