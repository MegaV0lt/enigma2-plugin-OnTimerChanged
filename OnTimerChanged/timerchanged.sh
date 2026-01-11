#!/bin/sh

# timerchanged.sh

# /usr/lib/enigma2/python/Plugins/Extensions/OnTimerChanged/timerchanged.sh
# This script is called by Enigma2 plugin OnTimerChanged when a timer status has changed.
# It receives two arguments:
# $1 - The new timer state (waiting, prepared, started, finished, failed, disabled)
# $2 - The recording filename without extension
# Example:
# timerchanged.sh 'started' '/media/hdd/movie/20260111 2000 - Das Erste - Tagesschau'


# Author: MegaV0lt @ Opena.tv

# Log the timer state change
LOG_FILE='/media/usb/logs/timerchanged.log'  # Path to the log file (/dev/null to disable logging)

STATE="$1"
RECORDING="$2"
[ -z "$RECORDING" ] && RECORDING='---Unknown---'
echo "Status changed for recording: $RECORDING" >> "$LOG_FILE"

case "$STATE" in
    waiting)  # TimerEntry.StateWaiting
        #echo "StateWaiting: $RECORDING" >> "$LOG_FILE"
        ;;
    prepared)  # TimerEntry.StatePrepared
        #echo "StatePrepared: $RECORDING" >> "$LOG_FILE"
        ;;
    started)  # TimerEntry.StateRunning
        echo "StateRunning: $RECORDING" >> "$LOG_FILE"
        ;;
    finished)  # TimerEntry.StateEnded
        echo "StateEnded: $RECORDING" >> "$LOG_FILE"
        ;;
    failed)  # TimerEntry.StateFailed
        #echo "StateFailed: $RECORDING" >> "$LOG_FILE"
        ;;
    disabled)  # TimerEntry.StateDisabled
        #echo "StateDisabled: $RECORDING" >> "$LOG_FILE"
        ;;
    *) echo "Unknown state $STATE for recording: $RECORDING" >> "$LOG_FILE" ;;
esac
