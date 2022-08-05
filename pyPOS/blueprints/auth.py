from pyPOS.utils.db import getDB
from pyPOS.utils.auth import authenticate
from pyPOS.utils.decorators import credentials_not_required
from flask import Blueprint, request, render_template, url_for, redirect, session, g, flash

bp = Blueprint( "auth", __name__, url_prefix="/auth" )

@bp.before_app_request
def load_logged_user():
    id = session.get( 'user_id' )
    if id:
        g.user = getDB().execute(
            'SELECT * FROM user WHERE id = ?', ( id, )
        ).fetchone()
    else:
        g.user = None

@bp.route( "/login", methods=("GET", "POST") )
@credentials_not_required
def login():
    error = None
    if request.method == "POST":
        username = request.form.get( 'username', None )
        password = request.form.get( 'password', None )
        error = authenticate( username, password )
        if not error:
            return redirect( url_for( "index.index" ) )
        flash( error )
    elif request.method == 'GET' and len( request.args.keys() ):
        username = request.args.get( 'username', None )
        password = request.args.get( 'password', None )
        error = authenticate( username, password )
        if not error:
            return redirect( url_for( "index.index" ) )
        flash( error )    
    return render_template( "auth/login.html" )

@bp.route( '/logout' )
def logout():
    session.clear()
    return redirect( url_for( "index.index" ) )

