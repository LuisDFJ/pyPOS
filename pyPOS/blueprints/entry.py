from flask import Blueprint, render_template, redirect, url_for, request
from pyPOS.utils.admin import get_products
from pyPOS.utils.order import get_order
from pyPOS.utils.entry import create_entry, modify_entry_status
from pyPOS.utils.decorators import user_domain_required, entry_status_required, credentials_level_required

bp = Blueprint( 'entry', __name__, url_prefix='/entry' )

@bp.route( '/<int:id>' )
@credentials_level_required( [ 'admin', 'user' ] )
@user_domain_required( [ 'Open' ] )
def index( id ):
    return render_template( 'entry/index.html', id=id, order=get_order( id ), products=get_products() )

@bp.route( '/<int:id>/add/<int:product_id>', methods=[ 'GET', 'POST' ] )
@credentials_level_required( [ 'admin', 'user' ] )
@user_domain_required( [ 'Open' ] )
def add( id, product_id ):
    if request.method == 'POST':
        comment = request.form[ 'comment' ]
        create_entry( id, product_id, comment )
        return redirect( url_for( 'order.modify', id=id ) )    
    return render_template( 'entry/add.html', product={'name':'food'} )

@bp.route( '/<int:id>/open/<int:product_id>' )
@credentials_level_required( [ 'admin', 'user' ] )
@user_domain_required( [ 'Open' ] )
@entry_status_required( [ 'Canceled' ] )
def open( id, product_id ):
    modify_entry_status( product_id, 'Created' )
    return redirect( url_for( 'order.modify', id=id ) )

@bp.route( '/<int:id>/deliver/<int:product_id>' )
@credentials_level_required( [ 'admin', 'user' ] )
@user_domain_required( [ 'Open' ] )
@entry_status_required( [ 'Ready' ] )
def deliver( id, product_id ):
    modify_entry_status( product_id, 'Delivered' )
    return redirect( url_for( 'order.modify', id=id ) )

@bp.route( '/<int:id>/cancel/<int:product_id>' )
@credentials_level_required( [ 'admin', 'user' ] )
@user_domain_required( [ 'Open' ] )
@entry_status_required( [ 'Created' ] )
def cancel( id, product_id ):
    modify_entry_status( product_id, 'Canceled' )
    return redirect( url_for( 'order.modify', id=id ) )