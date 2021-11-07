from pygwin._pg import pg as _pg
import os as _os
import tempfile as _tf

ffmpeg = None

class sound:
    def __init__(self, path):
        if not (path.endswith('.wav') or path.endswith('.ogg')):
            try:
                from pydub import AudioSegment as _as
                if ffmpeg != None:
                    _as.ffmpeg = ffmpeg
                    _as.converter = ffmpeg
                sound = _as.from_file(path, _os.path.splitext(path)[1])
                path = _tf.mkstemp('.wav')
                sound.export(path, format="wav")
            except:
                print('Set ffmpeg to path so that you don'+\
                      "'t have to convert the file to "+\
                      '".wav". If you have installed, but the error still appears, write down the path to ffmpeg.exe in plugin.ffmpeg.')
        self._sound = _pg.mixer.Sound(path)
    def play(self):
        self._sound.play()
    def stop(self):
        self._sound.stop()
    def volume():
        def fget(self):
            return self._sound.get_volume()
        def fset(self, value):
            if type(value) == int:
                self._sound.set_volume(value)
        def fdel(self):
            pass
        return locals()
    volume = property(**volume())
    @property
    def length(self):
        return self._sound.get_length()

class music:
    def __init__(self, path):
        if path.endswith('.wav') or path.endswith('.ogg'):
            self._path = path
        else:
            try:
                from pydub import AudioSegment as _as
                if ffmpeg != None:
                    _as.ffmpeg = ffmpeg
                    _as.converter = ffmpeg
                sound = _as.from_file(path, _os.path.splitext(path)[1])
                path = _tf.mkstemp('.wav')
                sound.export(path, format="wav")
            except:
                print('Set ffmpeg to path so that you don'+\
                      "'t have to convert the file to "+\
                      '".wav". If you have installed, but the error still appears, write down the path to ffmpeg.exe in plugin.ffmpeg.')
        _pg.mixer.music.load(path)
    def play(self, loops=0):
        _pg.mixer.music.play(loops)
    def stop(self):
        _pg.mixer.music.stop()
    def restart(self):
        _pg.mixer.music.rewind()
    def pause(self):
        _pg.mixer.music.pause()
    def release(self):
        _pg.mixer.music.unpause()
    def queue(self):
        _pg.mixer.music.queue(self._path)

    def volume():
        def fget(self):
            return _pg.mixer.music.get_volume()
        def fset(self, value):
            if type(value) == int:
                _pg.mixer.music.set_volume(value)
        def fdel(self):
            pass
        return locals()
    volume = property(**volume())

    def pos():
        def fget(self):
            return _pg.mixer.music.get_pos()
        def fset(self, value):
            if type(value) == int:
                _pg.mixer.music.set_pos(value)
        def fdel(self):
            pass
        return locals()
    pos = property(**pos())
