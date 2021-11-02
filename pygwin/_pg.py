from contextlib import contextmanager as _cm
import os as _os
import sys as _sys

@_cm
def _suppress_stdout():
    with open(_os.devnull, "w") as devnull:
        old_stdout = _sys.stdout
        _sys.stdout = devnull
        try:
            yield
        finally:
            _sys.stdout = old_stdout
with _suppress_stdout():
    import pygame as pg
    pg.init()
