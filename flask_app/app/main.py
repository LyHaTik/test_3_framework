# app/main.py
from flask import Flask
from .routes import bp as tasks_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(tasks_bp)
    return app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



