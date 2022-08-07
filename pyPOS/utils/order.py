import click
from typing         import OrderedDict
from flask.cli      import with_appcontext
from pyPOS.utils.db import getDB, openSQL

def modify_order_status( id:int, status:str ):
    db = getDB()
    try:
        db.execute(
            """ UPDATE orders
                SET status_id = (
                    SELECT id FROM order_status WHERE name = ?
                ) WHERE id = ?
            """,
            ( status, id )
        )
        db.commit()
    except db.IntegrityError:
        pass

def get_order( id:int ):
    db = getDB()
    return db.execute(
        openSQL( 'fetch_order_id.sql' ),
        ( id, )
    ).fetchone()

def get_order_by_status( user_id:int | None = None ):
    status_list = get_order_status()
    orders = OrderedDict()
    for status in status_list:
        orders[ status ] = get_orders( user_id=user_id, status=status )
    return orders

def get_orders( user_id:int | None = None, status:str | None = None ):
    db = getDB()
    if user_id and status:
        orders = db.execute(
            openSQL( 'fetch_order_user_status.sql' ),
            ( user_id, status )
        ).fetchall()
    elif user_id:
        orders = db.execute(
            openSQL( 'fetch_order_user.sql' ),
            ( user_id, )
        ).fetchall()
    elif status:
        orders = db.execute(
            openSQL( 'fetch_order_status.sql' ),
            ( status, )
        ).fetchall()
    else:
        orders = db.execute(
            openSQL( 'fetch_order.sql' )
        ).fetchall()
    return orders

def get_order_status():
    db = getDB()
    status = db.execute(
        'SELECT * FROM order_status'
    ).fetchall()
    return [ s['name'] for s in status ]

def create_order( name:str, user_id:int ):
    db = getDB()
    try:
        db.execute(
            openSQL( 'insert_order.sql' ),
            ( name, user_id )
        )
        db.commit()
    except db.IntegrityError:
        pass

@click.command( 'add-order' )
@click.option( '--name',    prompt=True )
@click.option( '--user-id', prompt=True, type=int )
@with_appcontext
def add_order_command( name:str, user_id:int ):
    create_order( name, user_id )
    click.echo( f'Order created [{name}]' )