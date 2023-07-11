from flask import Flask
import os
from dotenv import load_dotenv
from src.infrastructure.controllers.HttpCalendarController import calendar_API

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


def validate_service_address():
    assert PORT is not None, "env variable HOST not set"
    assert HOST is not None, "env variable PORT not set"


def create_app():
    validate_service_address()
    app_flask = Flask(__name__)
    app_flask.register_blueprint(calendar_API)
    return app_flask


if __name__ == '__main__':
    app = create_app()
    app.run(host=HOST, port=PORT)
