# try:
from pygwin.surface import surface
import pygwin.keyboard as keyboard
from pygwin.console import console
import pygwin.gamepad as _gp
import pygwin.mouse as mouse
from pygwin.rect import rect
import pygwin.image as image
import pygwin.mixer as mixer
from pygame.locals import *
import pygwin.font as font
from pygwin._win import *
from pygwin._pg import pg
import pygwin.ui as ui
gamepad = _gp.gamepad(pg)
# except ModuleNotFoundError as e:
#     import pip,os,sys
#     if 'imofpgw' in sys.argv:
#         os.system('cls' if os.name in ('nt', 'dos') else 'clear')
#         raise e
#     def install(package):
#         if hasattr(pip,'main'):pip.main(['install',package])
#         else:pip._internal.main(['install',package])
#         os.system('cls' if os.name in ('nt', 'dos') else 'clear')
#     modules = ['datetime',
#                'tempfile',
#                'pywin32',
#                'pickle',
#                'pygame',
#                'inputs',
#                'pydub',
#                'ctypes']
#     for i in modules:
#         install(i)
#     os.execv(sys.executable, ['python']+sys.argv+['imofpgw'])
