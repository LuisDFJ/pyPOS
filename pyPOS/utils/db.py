from math import prod
import os
import click
import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext

def getDB():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config[ 'DATABASE' ],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def closeDB( error = None ):
    db = g.pop( 'db', None )
    if db is not None:
        db.close()

def openSQL( file ):
    with current_app.open_resource( os.path.join( 'utils/sql', file ) ) as pFile:
        text = pFile.read()
    return text.decode( 'utf8' )

@click.command( 'init-db' )
@click.option( '--users', is_flag=True )
@click.option( '--products', is_flag=True )
@with_appcontext
def init_db_command( users, products ):
    """ Clear existing database. """
    db = getDB()
    if not products and not users: products = True; users = True
    if products:
        db.executescript( openSQL( 'create_products.sql' ) )
    if users:
        db.executescript( openSQL( 'create_users.sql' ) )
    click.echo( f'DATABASE Created: Users[{users}], Products[{products}]' )
