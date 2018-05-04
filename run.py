#!/usr/bin/env python
import os
import sys
import click
from dotenv import load_dotenv
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade
from app import create_app, db
from app.models import User, Role

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

COV = None
if os.environ.get('APP_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


app = create_app(os.getenv('APP_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                Role=Role)


@app.cli.command()
@click.option('--coverage/--no-coverage',
              default=False,
              help='Run tests under code coverage.')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('APP_COVERAGE'):
        import subprocess
        os.environ['APP_COVERAGE'] = '1'
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


@app.cli.command()
@click.option('--length',
              default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir',
              default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler"""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    upgrade()
    Role.insert_roles()
    User.insert_root_admin()


manager.add_command('shell', Shell(make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
