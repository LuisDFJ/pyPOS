from flask import Blueprint, render_template, redirect, url_for
from pyPOS.utils.decorators import credentials_level_required, user_domain_required, entry_status_required
from pyPOS.utils.entry import get_entry_by_status, modify_entry_status

bp = Blueprint( 'monitor', __name__, url_prefix='/monitor' )

@bp.route( '/' )
@credentials_level_required( [ 'admin', 'monitor' ] )
def index( ):
    print( dict( get_entry_by_status()['Created'][0] ) )
    return render_template( 'monitor/index.html', entry_dict=get_entry_by_status() )

# Created status

@bp.route( '/cancel/<int:id>/<int:product_id>' )
@credentials_level_required( [ 'admin', 'monitor' ] )
@user_domain_required( [ 'Open' ], [ 'admin', 'monitor' ] )
@entry_status_required( [ 'Created' ] )
def cancel( id, product_id ):
    modify_entry_status( product_id, 'Canceled' )
    return redirect( url_for( 'monitor.index' ) )

@bp.route( '/accept/<int:id>/<int:product_id>' )
@credentials_level_required( [ 'admin', 'monitor' ] )
@user_domain_required( [ 'Open' ], [ 'admin', 'monitor' ] )
@entry_status_required( [ 'Created' ] )
def accept( id, product_id ):
    modify_entry_status( product_id, 'In progress' )
    return redirect( url_for( 'monitor.index' ) )

# In progress status

@bp.route( '/ready/<int:id>/<int:product_id>' )
@credentials_level_required( [ 'admin', 'monitor' ] )
@user_domain_required( [ 'Open' ], [ 'admin', 'monitor' ] )
@entry_status_required( [ 'In progress' ] )
def ready( id, product_id ):
    modify_entry_status( product_id, 'Ready' )
    return redirect( url_for( 'monitor.index' ) )

# Delivered status

@bp.route( '/pay/<int:id>/<int:product_id>' )
@credentials_level_required( [ 'admin', 'monitor' ] )
@user_domain_required( [ 'Open' ], [ 'admin', 'monitor' ] )
@entry_status_required( [ 'Delivered' ] )
def pay( id, product_id ):
    modify_entry_status( product_id, 'Payed' )
    return redirect( url_for( 'monitor.index' ) )

# Canceled status

@bp.route( '/open/<int:id>/<int:product_id>' )
@credentials_level_required( [ 'admin', 'monitor' ] )
@user_domain_required( [ 'Open' ], [ 'admin', 'monitor' ] )
@entry_status_required( [ 'Canceled' ] )
def open( id, product_id ):
    modify_entry_status( product_id, 'Created' )
    return redirect( url_for( 'monitor.index' ) )
