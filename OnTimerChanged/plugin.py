# -*- coding: utf-8 -*-

# 'OnTimerChanged' Plugin for Enigma2 (Python 3)
# Description: Execute a script when a timer status changes
#
# Based on OnRecEnd by rdamas @ Opena.tv
# Modified by MegaV0lt @ Opena.tv
#   Runs on Enigma2 with Python3
#   Added handling for all TimerEntry states.
#   Added script for handling the different states

import os
import subprocess

from Plugins.Plugin import PluginDescriptor
from timer import TimerEntry

def TimerChange(timer):
    cmd = "/usr/lib/enigma2/python/Plugins/Extensions/OnTimerChanged/timerchanged.sh"
    print("[OnTimerChanged] TimerChange called")
    if os.path.isfile(cmd) and os.access(cmd, os.X_OK) and hasattr(timer, "Filename") and not timer.justplay and not timer.justremind:
        path, filename = os.path.split(timer.Filename)
        state_map = {
            TimerEntry.StateWaiting: "waiting",
            TimerEntry.StatePrepared: "prepared",
            TimerEntry.StateRunning: "started",
            TimerEntry.StateEnded: "finished",
            TimerEntry.StateFailed: "failed",
            TimerEntry.StateDisabled: "disabled",
        }
        if timer.state in state_map:
            print("[OnTimerChanged] TimerChange {0} recording: {1}".format(state_map[timer.state], filename))
            pid = subprocess.Popen([ cmd, state_map[timer.state], timer.Filename ]).pid
            print("[OnTimerChanged] has pid:", pid)

def autostart(reason, **kwargs):
    if "session" in kwargs and reason == 0:
        session = kwargs["session"]
        print("[OnTimerChanged] <START>")
        session.nav.RecordTimer.on_state_change.append(TimerChange)

def Plugins(**kwargs):
    return PluginDescriptor(
        name="OnTimerChanged",
        description="Aktion bei Statusänderung eines Timers",
        where = [PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART],
        fnc=autostart)
