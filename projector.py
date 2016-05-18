from __future__ import print_function
import serial
import time

class Button(object):
    # TODO: generate strings based on class introspection?
    UP = 'up'
    DOWN = 'down'

    BACK = 'back'
    ON = 'on'
    STANDBY = 'standby'
    INPUT = 'input'
    BRIGHTNESS = 'brightness'
    CONTRAST = 'contrast'

    SHARPNESS = 'sharpness'
    COLOR = 'color'
    TINT = 'tint'
    NR = 'noise_reduction'
    HIDE = 'hide'

    LENS_APERTURE = 'lens_aperture'
    MENU = 'menu'
    OK = 'ok'

    LENS = 'lens'
    RIGHT = 'right'
    LEFT = 'left'

    TEST = 'test'

    STAGE = 'stage'
    CINEMA2 = 'cinema2'
    CINEMA1 = 'cinema1'
    NATURAL = 'natural'
    DYNAMIC = 'dynamic'
    USER1 = 'user1'
    USER2 = 'user2'
    USER3 = 'user3'

    INFO = 'info'
    GAMMA = 'gamma'
    COLOR_TEMP = 'color_temp'
    ASPECT = 'aspect'

    CODES = {
        UP: b'\x30\x31',
        DOWN: b'\x30\x32',
        BACK: b'\x30\x33',
        ON: b'\x30\x35',
        STANDBY: b'\x30\x36',
        INPUT: b'\x30\x38',
        BRIGHTNESS: b'\x30\x39',
        CONTRAST: b'\x30\x41',

        SHARPNESS: b'\x31\x34',
        COLOR: b'\x31\x35',
        TINT: b'\x31\x36',
        NR: b'\x31\x38',
        HIDE: b'\x31\x44',

        LENS_APERTURE: b'\x32\x30',
        MENU: b'\x32\x45',
        OK: b'\x32\x46',

        LENS: b'\x33\x30',
        RIGHT: b'\x33\x34',
        LEFT: b'\x33\x36',

        TEST: b'\x35\x39',

        STAGE: b'\x36\x37',
        CINEMA2: b'\x36\x38',
        CINEMA1: b'\x36\x39',
        NATURAL: b'\x36\x41',
        DYNAMIC: b'\x36\x42',
        USER1: b'\x36\x44',
        USER2: b'\x36\x43',
        USER3: b'\x36\x45',

        INFO: b'\x37\x34',
        GAMMA: b'\x37\x35',
        COLOR_TEMP: b'\x37\x36',
        ASPECT: b'\x37\x37',
    }

class InputSource (object):
    S_VIDEO = 's-video'
    VIDEO = 'video'
    COMPUTER = 'computer'
    HDMI_1 = 'hdmi1'
    HDMI_2 = 'hdmi2'

    DISPLAY_NAMES = {
        S_VIDEO: 'S-Video',
        VIDEO: 'Video',
        COMPUTER: 'Computer',
        HDMI_1: 'HDMI 1',
        HDMI_2: 'HDMI 2'
    }

class ProjectorCommunicationError (Exception):
    pass

class Projector(object):
    # to be overwritten by child classes
    VALID_BUTTONS = []
    VALID_SOURCES = []

    def __init__ (self, port_url, unit_id=b'\x89\x01', timeout=1):
        self.url = port_url
        self.port = serial.serial_for_url (port_url,
            19200, parity='N', stopbits=1, timeout=timeout)

        self.unit_id = unit_id

    def send_operating (self, cmd, data=None, response_cmd=None):
        return self.send (b'\x21', cmd, data, response_cmd)

    def send_reference (self, cmd, data=None):
        was_ok = self.send (b'\x3f', cmd, data)

        # we don't get any data back
        if was_ok == True:
            return (was_ok, self.recv (cmd))
        else:
            return (was_ok, None)

    def send (self, header, cmd, data=None, response_cmd=None):
        footer = b'\x0A'
        if data:
            pkt = [header, self.unit_id, cmd, data, footer]
        else:
            pkt = [header, self.unit_id, cmd, footer]

        self.port.write (''.join (pkt))

        # check for the command we sent back out, unless another was specified
        if not response_cmd:
            response_cmd = cmd

        return self.recv (response_cmd)

    def recv (self, cmd):
        # 0x40 = response
        # 0x06 = ACK
        resp = self.port.readline()
        if not resp:
            raise ProjectorCommunicationError ("no response from projector")

        result_code = resp[0]
        if result_code == b'\x06':
            msgtype = 'ack'
        elif result_code == b'\x40':
            msgtype = 'data'
        else:
            raise ProjectorCommunicationError ("device returned unknown result code %r" % result_code)

        # ensure the unit ID matched
        response_unit_id = resp[1:3]
        if response_unit_id != self.unit_id:
            raise ProjectorCommunicationError ("device returned unknown unit id %r" % response_unit_id)

        response_cmd = resp[3:3+len(cmd)]
        if response_cmd != cmd:
            raise ProjectorCommunicationError ("device returned response command response %r for command %r" % (response_cmd, cmd))

        data = resp[3+len(cmd):-1] # don't include trailing \n

        if msgtype == 'data':
            return data
        elif msgtype == 'ack':
            return True
        elif msgtype == 'fail':
            return False
        else:
            raise ValueError ("invalid internal msgtype")

    @property
    def ready (self):
        return self.send_operating (b'\x00\x00')

    @property
    def mode(self):
        success, state = self.send_reference (b'\x50\x57')
        if not success:
            return None

        # note these are strings
        modes = {
            '\x30': 'standby',
            '\x31': 'power-on',
            '\x32': 'cool-down',
            '\x34': 'warning'
        }

        if state in modes:
            return modes[state]

        raise ValueError ("unknown power state " + repr(state))

    def turn_on(self):
        return self.send_operating (b'\x50\x57', b'\x31')

    def turn_off(self):
        return self.send_operating (b'\x50\x57', b'\x30')

    def set_input(self, mode):
        # this command is only valid when powered on
        if self.mode != 'power-on':
            return False

        video_states = {
            InputSource.S_VIDEO: '\x30',
            InputSource.VIDEO: '\x31',
            InputSource.COMPUTER: '\x32',
            InputSource.HDMI_1: '\x36',
            InputSource.HDMI_2: '\x37'
        }

        if mode not in video_states:
            return ValueError ("invalid input " + repr(mode))

        cmd_state = video_states[mode]
        return self.send_operating(b'\x49\x50', cmd_state)

    def press_button(self, btn):
        if btn not in self.VALID_BUTTONS:
            raise ValueError ("unsupported button " + repr(btn))

        # this command is not in standby
        # if self.mode == 'standby':
        #     return None

        return self.send_operating(b'\x52\x43\x37\x33',
            Button.CODES[btn], response_cmd='\x52\x43')

    @property
    def input(self):
        # this command is only valid when powered on
        if self.mode != 'power-on':
            return None

        success, state = self.send_reference (b'\x49\x50')
        if not success:
            return None

        # note these are strings
        video_states = {
            '\x30': InputSource.S_VIDEO,
            '\x31': InputSource.VIDEO,
            '\x32': InputSource.COMPUTER,
            '\x36': InputSource.HDMI_1,
            '\x37': InputSource.HDMI_2
        }

        if state in video_states:
            return video_states[state]

        raise ValueError ("unknown video state " + repr(state))

    @property
    def model(self):
        return self.send_operating(b'\x4d\x44')

class HD250 (Projector):
    VALID_SOURCES = [
        InputSource.S_VIDEO,
        InputSource.VIDEO,
        InputSource.COMPUTER,
        InputSource.HDMI_1,
        InputSource.HDMI_2
    ]

    VALID_BUTTONS = [
        Button.UP,
        Button.DOWN,
        Button.BACK,
        Button.ON,
        Button.STANDBY,
        Button.INPUT,
        Button.BRIGHTNESS,
        Button.CONTRAST,
        Button.SHARPNESS,
        Button.COLOR,
        Button.TINT,
        Button.NR,
        Button.HIDE,
        Button.LENS_APERTURE,
        Button.MENU,
        Button.OK,
        Button.LENS,
        Button.RIGHT,
        Button.LEFT,
        Button.TEST,
        Button.STAGE,
        Button.CINEMA2,
        Button.CINEMA1,
        Button.NATURAL,
        Button.DYNAMIC,
        Button.USER1,
        Button.USER2,
        Button.USER3,
        Button.INFO,
        Button.GAMMA,
        Button.COLOR_TEMP,
        Button.ASPECT,
    ]

    @property
    def model(self):
        return 'DLA-HD250'

if __name__ == '__main__':
    p = HD250 ('/dev/ttyUSB0')

    if p.ready:
        print ("currently in", p.mode, "mode")
        print ("viewing input", p.input)
        print ("model", p.model)

        p.press_button (Button.BACK) # dismiss lamp warning
        # p.turn_on()
        # time.sleep (35) # let the projector warm up
    else:
        print ("device not ready yet")