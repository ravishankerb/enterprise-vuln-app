from flask import Flask


def create_app():
    app = Flask(__name__)
    # Insecure configuration (DEBUG on, secret in source)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'super-secret-key-12345' # insecure: hardcoded secret


    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    return app