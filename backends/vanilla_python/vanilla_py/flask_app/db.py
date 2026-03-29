import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext
from . import seed_data
import click 
from pathlib import Path
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db=g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    if (Path(current_app.config['DATABASE']).exists()):
        print ("Database already exist")
        pass
    else :
        print ("Initialise New Database")
        db = get_db()
        #Initialize the structure of the db
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
        #Initialize the static information (bow types/ round types)
        seed_data.seed_db_static_information()
        #Initialize the user related information
        seed_data.seed_db_user_related_data()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
