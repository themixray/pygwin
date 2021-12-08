from contextlib import contextmanager
from pygwin._pg import pg as _pg
import moviepy.editor as mpe
from array import array
from PIL import Image
import numpy as np
import threading
import pyautogui
import tempfile
import pyaudio
import wave
import time
import sys
import cv2
import os

class record:
    def __init__(self,win,audio=False):
        self._isaudio = audio
        self._surface = win
        self.reset()
    def reset(self):
        self._run = False
        self._fpss = []
        self._frames = []
        self._codec = cv2.VideoWriter_fourcc(*"mp4v")
        if self._isaudio:
            self._apy = pyaudio.PyAudio()
            self._aframs = []
            self._astrm = self.apy.open(format=pyaudio.paInt16,channels=1,
                             rate=44100,input=True,frames_per_buffer=1024)
    def start(self,newThread=True):
        self._run = True
        if self._isaudio:
            def audiot(self):
                while self._run:
                    self._aframs.append(self.astrm.read(1024))
            self._athread = threading.Thread(target=lambda:audiot(self))
            self._athread.start()
        def main(self):
            while self.run:
                self._record()
        if newThread:
            self._thread = threading.Thread(target=lambda:main(self))
            self._thread.start()
        else:main()
    def _record(self):
        if self._run:
            try:
                self._frames.append(self._surface)
                self._fpss.append(self._surface.rawFps)
            except:
                pass
    def render(self, path):
        temp = tempfile.gettempdir()
        if self.isaudio:
            wavpath = os.path.join(temp, 'audio.wav')
            wavfile = wave.open(wavpath, 'wb')
            wavfile.setnchannels(1)
            wavfile.setsampwidth(self._apy.get_sample_size(pyaudio.paInt16))
            wavfile.setframerate(44100)
            af = []
            for i in self._aframs:
                af.append(array('h',i))
            wavfile.writeframes(b''.join(af))
            wavfile.close()

        fps = 0
        for i in self._fpss:
            fps += i
        fps = fps/len(self._fpss)
        if self._isaudio:
            noaudiopath = os.path.join(temp, 'noaudio.mp4')
        else:
            noaudiopath = path
        out = cv2.VideoWriter(noaudiopath,self._codec,
                              fps,self._surface.size)
        for i in self._frames:
            frame = np.array(_pg.surfarray.array3d(i).swapaxes(0,1))
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            out.write(frame)
        out.release()

        if self._isaudio:
            videoclip = mpe.VideoFileClip(noaudiopath)
            audioclip = mpe.AudioFileClip(wavpath)
            new_audioclip = mpe.CompositeAudioClip([audioclip])
            videoclip.audio = new_audioclip
            @contextmanager
            def ss():
                with open(os.devnull, "w") as devnull:
                    oso = sys.stdout
                    sys.stdout = devnull
                    try:yield
                    finally:sys.stdout=oso
            with ss():
                videoclip.write_videofile(path)
            os.remove(noaudiopath)
            os.remove(wavpath)
    def stop(self):
        self._run = False
        try:
            self._thread.join()
        except:
            pass
        if self._isaudio:
            self._athread.join()
