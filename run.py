#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade
from app import create_app, db

from app.models.User import User
from app.models.Role import Role
from app.models.App import App
from app.models.Api import Api
from app.models.ApiGroup import ApiGroup
from app.models.ApiResponse import ApiResponse
from app.models.ApiExample import ApiExample
from app.models.Log import Log


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

COV = None
if os.getenv('APP_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.getenv('APP_CONFIG', 'default'))


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                User=User, Role=Role, App=App, Api=Api, ApiGroup=ApiGroup,
                ApiResponse=ApiResponse, ApiExample=ApiExample, Log=Log)


manager = Manager(app)
manager.add_command('shell', Shell(make_shell_context))

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def routes():
    """Helper to list routes."""
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:30s} {:50s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.getenv('APP_COVERAGE'):
        import subprocess
        sys.exit(subprocess.call(sys.argv))

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        coverage_dir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=coverage_dir)
        print('HTML version: file://%s/index.html' % coverage_dir)
        COV.erase()


@manager.command
def profile(length, profile_dir):
    """Start the application under the code profiler"""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    """Run deployment tasks."""
    upgrade()
    Role.insert_roles()
    User.insert_root_admin()


if __name__ == '__main__':
    manager.run()
