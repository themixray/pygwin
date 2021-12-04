import inputs as _inputs
import threading as _threading
import time as _time

class gamepad:
    def __init__(self, pygame):
        self._lasty = ''
        self._lastx = ''
        self.founded = False
        self._buttons = {'left-joystick': False,
                         'right-joystick': False,
                         'north': False,
                         'south': False,
                         'west': False,
                         'east': False,
                         'l1': False,
                         'l2': False,
                         'r1': False,
                         'r2': False,
                         'up': False,
                         'down': False,
                         'left': False,
                         'right': False,
                         'start': False,
                         'select': False}
        self.leftJoystick = [0, 0]
        self.rightJoystick = [0, 0]
        self._pygame = pygame
        self._start()
    def _tick(self):
        try:
            events = _inputs.get_gamepad()
        except:
            return
        if not self._pygame.display.get_active():
            return
        self.founded = True
        if events:
            for event in events:
                if event.code == 'ABS_X':
                    self.leftJoystick[0] = event.state
                elif event.code == 'ABS_Y':
                    self.leftJoystick[1] = event.state
                elif event.code == 'ABS_RY':
                    self.rightJoystick[1] = event.state
                elif event.code == 'ABS_RX':
                    self.rightJoystick[0] = event.state
                elif event.code == 'BTN_THUMBL':
                    self._buttons['left-joystick'] = event.state
                elif event.code == 'BTN_THUMBR':
                    self._buttons['right-joystick'] = event.state
                elif event.code == 'BTN_TL':
                    self._buttons['l1'] = event.state
                elif event.code == 'BTN_TR':
                    self._buttons['r1'] = event.state
                elif event.code == 'ABS_Z':
                    if event.state == 255:
                        self._buttons['l2'] = 1
                    elif event.state == 0:
                        self._buttons['l2'] = 0
                elif event.code == 'ABS_RZ':
                    if event.state == 255:
                        self._buttons['r2'] = 1
                    elif event.state == 0:
                        self._buttons['r2'] = 0
                elif event.code == 'BTN_WEST':
                    self._buttons['west'] = event.state
                elif event.code == 'BTN_NORTH':
                    self._buttons['north'] = event.state
                elif event.code == 'BTN_EAST':
                    self._buttons['east'] = event.state
                elif event.code == 'BTN_SOUTH':
                    self._buttons['south'] = event.state
                elif event.code == 'ABS_HAT0Y':
                    if event.state == 1:
                        self._buttons['down'] = True
                        self._lasty = 'down'
                    elif event.state == -1:
                        self._buttons['up'] = True
                        self._lasty = 'up'
                    else:
                        self._buttons[self._lasty] = False
                elif event.code == 'ABS_HAT0X':
                    if event.state == 1:
                        self._buttons['right'] = True
                        self._lastx = 'right'
                    elif event.state == -1:
                        self._buttons['left'] = True
                        self._lastx = 'left'
                    else:
                        self._buttons[self._lastx] = False
                elif event.code == 'BTN_START':
                    self._buttons['select'] = event.state
                elif event.code == 'BTN_SELECT':
                    self._buttons['start'] = event.state
    def _start(self):
        self.founded = False
        self._started = True
        def ttcb(self):
            while self._started:
                self._tick()
        _threading.Thread(target=lambda:ttcb(self),daemon=True).start()
    def close(self):
        self._started = False
    def isPressed(self, btn):
        return btn in self._buttons
    def reset(self):
        self._lasty = ''
        self._lastx = ''
        self._buttons = []
        self.leftJoystick = [0, 0]
        self.rightJoystick = [0, 0]
    def getPressed(self):
        return self._buttons
