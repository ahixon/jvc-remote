from flask import Flask, abort, jsonify, render_template
from projector import Button, InputSource, HD250, ProjectorCommunicationError
from itertools import izip
from functools import wraps

app = Flask(__name__, template_folder='.')
projector = None

def projector_command (f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ProjectorCommunicationError:
            abort (503, 'Could not communicate with projector "%s". '
                'Is it connected and powered on?' % projector.url)
    return decorated

# information only (this may change if we
# implement an auto-instanciated projector class)
@app.route('/buttons')
def view_buttons():
    return jsonify({'names': projector.VALID_BUTTONS})

@app.route ('/inputs')
def view_inputs():
    return jsonify(dict(izip (projector.VALID_SOURCES,
        map (lambda src: InputSource.DISPLAY_NAMES[src], projector.VALID_SOURCES))))

@app.route('/press/<button>')
@projector_command
def press(button):
    button = button.lower()
    if button not in Button.CODES:
        abort (404, 'No such button ' + button)

    return jsonify({'success': projector.press_button (button)})

@app.route ('/status')
@projector_command
def status():
    return jsonify({
        'mode': projector.mode,
        'input': projector.input,
        'model': projector.model
    })

@app.route ('/input/<source>')
@projector_command
def set_input(source):
    source = source.lower()
    if source not in projector.VALID_SOURCES:
        abort (404, 'Invalid mode ' + source)

    return jsonify({'success': projector.set_input(source)})

@app.route('/on')
@projector_command
def on():
    return jsonify({'success': projector.turn_on()})

@app.route('/off')
@projector_command
def off():
    return jsonify({'success': projector.turn_off()})

@app.route('/')
def index():
    return render_template ('index.html',
        sources=projector.VALID_SOURCES,
        input_names=InputSource.DISPLAY_NAMES,
        state={
            'mode': projector.mode,
            'input': projector.input,
            'model': projector.model
        })

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write ("Usage: %s [serial device]\n" % sys.argv[0])
    else:
        projector = HD250 (sys.argv[1], timeout=0.4)
        app.run(host='0.0.0.0')