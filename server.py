from wsgiref.simple_server import make_server
from sys import exc_info
from traceback import format_tb
from wsgiref.util import request_uri, shift_path_info
from projector import Button, InputSource, HD250, ProjectorCommunicationError
from itertools import izip
from functools import wraps
import json

projector = None

class WebException (Exception):
    def __init__ (self, code, msg=None):
        self.code = code
        default_msgs = {
            '404 Not Found': 'The requested resource could not be found.',
            '503 Service Unavailable': 'The underlying service is not '
                                       'available.',
            '500 Internal Server Error': 'An internal exception occured.'
        }

        if not msg:
            if code in default_msgs:
                self.msg = default_msgs[code]
            else:
                self.msg = ''
        else:
            self.msg = msg

    def __repr__ (self):
        if not self.msg:
            return self.code
        return '%s: %s' % (self.code, self.msg)

    def __str__ (self):
        return '<h1>%s</h1><p>%s</p>' % (self.code, self.msg)

def projector_command (f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ProjectorCommunicationError:
            raise WebException ('503 Service Unavailable', 'Could not '
                'communicate with projector "%s". Is it connected and '
                'powered on?' % projector.url)
    return decorated

# information only (this may change if we
# implement an auto-instanciated projector class)
def view_buttons():
    return json.dumps({'names': projector.VALID_BUTTONS})

def view_inputs():
    return json.dumps(dict(izip (projector.VALID_SOURCES,
        map (lambda src: InputSource.DISPLAY_NAMES[src],
                         projector.VALID_SOURCES))))

@projector_command
def press(button):
    button = button.lower()
    if button not in Button.CODES:
        abort ('404 Not Found', 'No such button ' + button)

    return json.dumps({'success': projector.press_button (button)})

@projector_command
def projector_status():
    return json.dumps({
        'mode': projector.mode,
        'input': projector.input,
        'model': projector.model
    })

@projector_command
def set_input(source):
    source = source.lower()
    if source not in projector.VALID_SOURCES:
        raise WebException ('404 Not Found', 'Invalid mode ' + source)

    return json.dumps({'success': projector.set_input(source)})

@projector_command
def on():
    return json.dumps({'success': projector.turn_on()})

@projector_command
def off():
    return json.dumps({'success': projector.turn_off()})

def index():
    return open ('index.html', 'rb')

def remote_webapp (environ, start_response):
    routes = {
        'buttons': view_buttons,
        'inputs': view_inputs,
        'press': lambda: press_button(shift_path_info (environ)),
        'status': projector_status,
        'input': lambda: set_input(shift_path_info (environ)),
        'on': on,
        'off': off,
        '': index
    }

    result = None
    base_path = shift_path_info (environ)
    if base_path not in routes:
        status = '404 Not Found'
        headers = [('Content-type', 'text/html')]
        result = str(WebException (status))
    else:
        try:
            handler = routes[base_path]
            result = handler()
            status = '200 OK'  # HTTP Status
            if type(result) != str and type(result) != unicode:
                headers = [('Content-type', 'text/html')] 
            else:
                headers = [('Content-type', 'application/json')]
        except WebException, ex:
            status = ex.status
            headers = [('Content-type', 'text/html')] 
            result = str(ex)
        except:
            status = '500 Internal Server Error'
            headers = [('Content-type', 'text/html')] 
            e_type, e_value, tb = exc_info()
            html = ('An internal exception occured. The stacktrace was: '
                   '</p><pre>%s\n%s</pre><p>' % (
                        ''.join (format_tb(tb)),
                        '%s: %s' % (e_type.__name__, e_value)))
            result = str(WebException (status, html))
        
    start_response(status, headers)

    return result

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write ("Usage: %s [serial device]\n" % sys.argv[0])
    else:
        projector = HD250 (sys.argv[1], timeout=0.4)
        httpd = make_server('', 8000, remote_webapp)
        print "Serving on port 8000..."

        # Serve until process is killed
        httpd.serve_forever()