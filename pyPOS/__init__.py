import os
from flask import Flask
from pyPOS.utils.db     import init_db_command, closeDB
from pyPOS.utils.auth   import create_user_command, gen_tokens_command, user_authentication_command
from pyPOS.blueprints   import index
from pyPOS.blueprints   import auth


def init_app( app : Flask ):
    # Teardown registration
    app.teardown_appcontext( closeDB )
    # Commands registration
    app.cli.add_command( init_db_command )
    app.cli.add_command( create_user_command )
    app.cli.add_command( gen_tokens_command )
    app.cli.add_command( user_authentication_command )
    # Blueprints registration
    app.register_blueprint( index.bp )
    app.register_blueprint( auth.bp )

def create_app():
    app = Flask( __name__, instance_relative_config=True )

    try:
        os.makedirs( app.instance_path )
    except OSError:
        pass

    app.config.from_mapping(
        SECRET_KEY = 'dev_key',
        DATABASE = os.path.join( app.instance_path, 'db.sqlite' ),
        TOKEN_LENGTH = 6
    )

    app.config.from_pyfile(
        'config.py',
        silent = True
    )

    init_app( app )

    return app