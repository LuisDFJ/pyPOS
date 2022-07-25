import click
from flask import current_app
from flask.cli import with_appcontext
from pyPOS.utils.db import getDB
from typing import OrderedDict

CATEGORIES = [ 'Food', 'Drink' ]

def get_products():
    db = getDB()
    products = OrderedDict()
    for category in CATEGORIES:
        products[ category ] = db.execute(
            'SELECT * FROM product WHERE category = ?',
            ( category, )
        ).fetchall()
    return products


@click.command( 'add-product' )
@click.option( '--name', prompt=True )
@click.option( '--price', prompt=True )
@click.option( '--category', prompt=True, type=click.Choice( CATEGORIES ) )
@click.option( '--description', prompt=True )
@click.option( '--thumbnail', prompt=True )
@with_appcontext
def add_product_command( name, price, category, description, thumbnail ):
    db = getDB()
    db.execute(
        'INSERT INTO product ( name, price, category, description, thumbnail ) VALUES ( ?, ?, ?, ?, ? )',
        ( name, float(price), category, description, thumbnail )
    )
    db.commit()