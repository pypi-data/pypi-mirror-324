# web_time_server/server.py
from flask import Flask
import datetime

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def show_time():
        return {'time': datetime.datetime.now().isoformat()}

    return app

def run_server():
    app = create_app()
    app.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    run_server()

