from flask import Blueprint, render_template, redirect, url_for, request
from pyPOS.utils.decorators import user_domain_required
from pyPOS.utils.admin import get_product
from pyPOS.utils.order import get_order, create_entry

bp = Blueprint( 'entry', __name__, url_prefix='/entry' )

@bp.route( '/<int:id>' )
@user_domain_required( [ 'Open' ] )
def index( id ):
    return render_template( 'entry/index.html', id=id, order=get_order( id ), product_list=get_product() )

@bp.route( '/<int:id>/add/<int:product_id>', methods=[ 'GET', 'POST' ] )
@user_domain_required( [ 'Open' ] )
def add( id, product_id ):
    if request.method == 'POST':
        comment = request.form[ 'comment' ]
        create_entry( id, product_id, comment )
        return redirect( url_for( 'order.modify', id=id ) )    
    return render_template( 'entry/add.html', product={'name':'food'} )

