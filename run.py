from sign_language_interpreter.app import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, use_reloader=False)