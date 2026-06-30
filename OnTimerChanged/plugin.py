# -*- coding: utf-8 -*-

# 'OnTimerChanged' Plugin for Enigma2 (Python 3)
# Description: Execute a script when a timer status changes
#
# Based on OnRecEnd by rdamas @ Opena.tv
# Modified by MegaV0lt @ Opena.tv
#   Runs on Enigma2 with Python3
#   Added handling for all TimerEntry states.
#   Added script for handling the different states

from os import access, X_OK
from os.path import isfile, split

from Components.Task import Job, Task, job_manager
from Plugins.Plugin import PluginDescriptor
from timer import TimerEntry

def TimerChange(timer):
    cmd = "/usr/lib/enigma2/python/Plugins/Extensions/OnTimerChanged/timerchanged.sh"
    print("[OnTimerChanged] TimerChange called")
    if isfile(cmd) and access(cmd, X_OK) and hasattr(timer, "Filename") and not timer.justplay and not timer.justremind:
        path, filename = split(timer.Filename)
        state_map = {
            TimerEntry.StateWaiting: "waiting",
            TimerEntry.StatePrepared: "prepared",
            TimerEntry.StateRunning: "started",
            TimerEntry.StateEnded: "finished",
            TimerEntry.StateFailed: "failed",
            TimerEntry.StateDisabled: "disabled",
        }

        if timer.state in state_map:
            state = state_map[timer.state]
            print(f"[OnTimerChanged] TimerChange {state} recording: {filename}")
            job = Job(f"OnTimerChanged: {state} {filename}")
            task = Task(job, "timerchanged.sh")
            task.setCommandline(cmd, [cmd, state, timer.Filename])
            job_manager.AddJob(job, onFail=lambda *_: None)

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
