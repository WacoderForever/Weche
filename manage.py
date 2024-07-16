#!/usr/bin/env python3

import os
from app import create_app, db
from app.models import User, Role
from flask.cli import FlaskGroup
from dotenv import load_dotenv

load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG','default'))
cli=FlaskGroup(create_app=lambda: app)

@app.shell_context_processor
def make_shell_context():
    with app.app_context():
        return {
            'app': app,
            'db': db,
            'User': User,
            'Role': Role
        }

if __name__ == '__main__':
    cli.main(['run', '--host', '0.0.0.0', '--port', '8080']) 

