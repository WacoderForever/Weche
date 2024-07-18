#!/usr/bin/env python3

import os
from app import create_app, db
from app.models import User, Role
from flask.cli import FlaskGroup
from dotenv import load_dotenv

load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
cli=FlaskGroup(create_app=lambda: app)

@cli.command("test")
def test():
    "Run unit tests"
    os.environ['FLASK_CONFIG'] = 'testing'
    import unittest
    tests=unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@cli.command("init_db")
def init_db():
    with app.app_context():
        db.create_all()

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
    os.environ['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')
    os.environ['FLASK_TEST'] = os.getenv('FLASK_TEST', '1')
    cli()

