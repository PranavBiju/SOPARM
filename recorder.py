#!/usr/bin/env python3

import tempfile
import queue
import sys
from datetime import datetime
import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)
from usbmonitor import USBMonitor

q = queue.Queue()
samplerate = 41440
channels =1
subtype = "PCM_24"
current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
str_current_datetime = str(current_datetime)
pre = 'audio_file_'+current_datetime
pre = pre.replace(" ", "")
filename = tempfile.mktemp(prefix=pre, suffix='.wav', dir='/home/alpha3/Desktop/Arm_project/24-25 sem1/Final pipeline/uploads/')
def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())
monitor = USBMonitor(filter_devices=({'ID_MODEL': 'USB_PnP_Sound_Device'}, {'ID_VENDOR_ID': '08bb', 'ID_MODEL_ID': '2902'}))

# Get the current devices
devices_dict = monitor.get_available_devices()
while True:
    #print("waitng")
    devices_dict = monitor.get_available_devices()
    if devices_dict :
        try:
            # Make sure the file is opened before recording anything:
            with sf.SoundFile(filename, mode='x', samplerate=samplerate,channels=channels, subtype=subtype) as file:
                with sd.InputStream(samplerate=samplerate,channels=channels, callback=callback):
                    # Flush stale audio buffer for 0.5 seconds
                    import time as _time
                    flush_end = _time.time() + 0.5
                    while _time.time() < flush_end:
                        try:
                            q.get(timeout=0.05)
                        except queue.Empty:
                            pass
                    # Clear any remaining stale data
                    while not q.empty():
                        q.get_nowait()
                    print('#' * 80)
                    print('#' * 80)
                    while monitor.get_available_devices():
                        file.write(q.get())

        finally:
            print('\nRecording finished: ' + repr(filename))
            break
