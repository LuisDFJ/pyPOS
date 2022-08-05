import click
from flask.cli                  import with_appcontext
from pyPOS.utils.db             import getDB
from pyPOS.utils.products       import get_categories, get_root_node
from pyPOS.utils.click_utils    import ClickProductContext, ClickProductChoiceContext, ClickProductChoice

ALLOWED_EXTENSIONS = [ 'jpg', 'jpeg', 'png' ]

def allowed_file( filename:str ):
    return '.' in filename and filename.rsplit( '.', 1 )[1].lower() in ALLOWED_EXTENSIONS

def get_users():
    db = getDB()
    users = db.execute(
        "SELECT username FROM user WHERE position = 'user'"
    ).fetchall()
    user_list = []
    for user in users:
        user_list.append( user[ 'username' ] )
    return user_list

def get_products():
    db = getDB()
    productNode = get_root_node()
    for category in get_categories():
        products = db.execute(
            'SELECT * FROM product WHERE category = ?',
            ( category, )
        ).fetchall()
        productNode[ category ].insert( products )
    products_list = productNode.unwrap()
    products_list.pop( 0 )
    return products_list

def get_product( id:int | None = None ):
    db = getDB()
    if id:
        return db.execute(
            'SELECT * FROM product WHERE id = ?',
            ( id, )
        ).fetchone()
    return db.execute( 'SELECT * FROM product' ).fetchall()

def add_product( name:str, price:float, category:str, description:str, thumbnail:str ):
    db = getDB()
    try:
        db.execute(
            'INSERT INTO product ( name, price, category, description, thumbnail ) VALUES ( ?, ?, ?, ?, ? )',
            ( name, price, category, description, thumbnail )
        )
        db.commit()
    except db.IntegrityError:
        return 'Error: Repeated name'

def modify_product( id:int, name:str = "", price:float = None, category:str = "", description:str = "", thumbnail:str = "" ):
    attributes_map = {
        'name': name,
        'price': price,
        'category': category,
        'description': description,
        'thumbnail': thumbnail
    }
    db = getDB()
    for key, val in attributes_map.items():
        if val:
            db.execute(
                f'UPDATE product SET {key} = ? WHERE id = ?',
                ( val, id )
            )
    db.commit()

def delete_product( id:int ):
    db = getDB()
    db.execute(
        'DELETE FROM product WHERE id = ?',
        ( id, )
    )
    db.commit()

@click.command( 'add-product' )
@click.option( '--name',        prompt=True )
@click.option( '--price',       prompt=True, type=float )
@click.option( '--category',    prompt=True, cls=ClickProductChoice, type=click.Choice( [] ) )
@click.option( '--description', prompt=True )
@click.option( '--thumbnail',   prompt=True )
@with_appcontext
def add_product_command( name, price, category, description, thumbnail ):
    add_product( name, price, category, description, thumbnail )

@click.command( 'modify-product' )
@click.option( '--id',          prompt=True, type=int )
@click.option( '--name',        prompt=True, cls=ClickProductContext, get_product_callback=get_product )
@click.option( '--price',       prompt=True, cls=ClickProductContext, get_product_callback=get_product, type=float )
@click.option( '--category',    prompt=True, cls=ClickProductChoiceContext, get_product_callback=get_product, type=click.Choice( [] ) )
@click.option( '--description', prompt=True, cls=ClickProductContext, get_product_callback=get_product )
@click.option( '--thumbnail',   prompt=True, cls=ClickProductContext, get_product_callback=get_product )
@with_appcontext
def modify_product_command( **kwargs ):
    modify_product( **kwargs )

@click.command( 'delete-product' )
@click.option( '--id',          prompt=True, type=int )
@with_appcontext
def delete_product_command( id ):
    delete_product( id )