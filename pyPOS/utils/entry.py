import click
from typing         import OrderedDict
from flask.cli      import with_appcontext
from pyPOS.utils.db import getDB, openSQL

def modify_entry_status( id:int, status:str, order:bool = False ):
    db = getDB()
    try:
        if order:
            db.execute(
                """ UPDATE order_entry
                    SET status_id = (
                        SELECT id FROM order_entry_status WHERE name = ?
                    ) WHERE order_id = ?
                """,
                ( status, id )
            )
            db.commit()
        else:
            db.execute(
                """ UPDATE order_entry
                    SET status_id = (
                        SELECT id FROM order_entry_status WHERE name = ?
                    ) WHERE id = ?
                """,
                ( status, id )
            )
            db.commit()
    except db.IntegrityError:
        pass

def get_entry( id:int ):
    db = getDB()
    return db.execute(
        'SELECT * FROM entry_view WHERE id = ?',
        ( id, )
    ).fetchone()

def get_entry_by_status( order_id : int | None = None ):
    status_list = get_entry_status()
    entries = OrderedDict()
    for status in status_list:
        entries[ status ] = get_entries( id=order_id, status=status )
    return entries

def get_entries( id:int | None = None, status:str | None = None ):
    db = getDB()
    if status and id:
        return db.execute(
            'SELECT * FROM entry_view WHERE order_id = ? AND status = ?',
            ( id, status )
        ).fetchall()
    elif id:
        return db.execute(
            'SELECT * FROM entry_view WHERE order_id = ?',
            ( id, )
        ).fetchall()
    elif status:
        return db.execute(
            'SELECT * FROM entry_view WHERE status = ?',
            ( status, )
        ).fetchall()
    else:
        return db.execute(
            'SELECT * FROM entry_view'
        ).fetchall()

def get_entry_status():
    db = getDB()
    status = db.execute(
        'SELECT * FROM order_entry_status'
    ).fetchall()
    return [ s['name'] for s in status ]

def create_entry( id:int, product_id:int, comment:str ):
    db = getDB()
    try:
        db.execute(
            openSQL( 'insert_entry.sql' ),
            ( id, product_id, comment )
        )
        db.commit()
    except db.IntegrityError:
        pass

@click.command( 'add-entry' )
@click.option( '--id',          prompt=True, type=int )
@click.option( '--product-id',  prompt=True, type=int )
@click.option( '--comment',     prompt=True )
@with_appcontext
def add_entry_command( id:int, product_id:int, comment:str ):
    create_entry( id, product_id, comment )
    click.echo( f'Entry created [{id}]' )