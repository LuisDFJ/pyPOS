import os
from flask import Flask
#from dotenv import load_dotenv
from pyPOS.blueprints   import auth
from pyPOS.blueprints   import index
from pyPOS.blueprints   import entry
from pyPOS.blueprints   import orders
from pyPOS.blueprints   import monitor
from pyPOS.blueprints   import admin_users
from pyPOS.blueprints   import admin_products
from pyPOS.utils.db     import init_db_command, closeDB
from pyPOS.utils.auth   import create_user_command, delete_user_command, gen_tokens_command
from pyPOS.utils.admin  import add_product_command, modify_product_command, delete_product_command
from pyPOS.utils.order  import add_order_command
from pyPOS.utils.entry  import add_entry_command

def init_app( app : Flask ):
    # Teardown registration
    app.teardown_appcontext( closeDB )
    # Commands registration
    app.cli.add_command( init_db_command )
    app.cli.add_command( create_user_command )
    app.cli.add_command( delete_user_command )
    app.cli.add_command( gen_tokens_command )
    app.cli.add_command( add_product_command )
    app.cli.add_command( modify_product_command )
    app.cli.add_command( delete_product_command )
    app.cli.add_command( add_order_command )
    app.cli.add_command( add_entry_command )
    # Blueprints registration
    app.register_blueprint( auth.bp )
    app.register_blueprint( index.bp )
    app.register_blueprint( entry.bp )
    app.register_blueprint( orders.bp )
    app.register_blueprint( monitor.bp )
    app.register_blueprint( admin_users.bp )
    app.register_blueprint( admin_products.bp )


def create_app():
    app = Flask( __name__, instance_relative_config=True )

    try:
        os.makedirs( app.instance_path )
    except OSError:
        pass

    app.config.from_mapping(
        SECRET_KEY = 'dev_key',
        DATABASE = os.path.join( app.instance_path, 'db.sqlite' ),
        TOKEN_LENGTH = 6,
        PRODUCT_CATEGORIES = [ 'Food', 'Drink' ],
    )

    app.config.from_pyfile(
        'config.py',
        silent = True
    )

    init_app( app )

    return app