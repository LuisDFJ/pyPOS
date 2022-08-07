from flask                  import Blueprint, render_template, g, request, redirect, url_for
from pyPOS.utils.order      import get_order_by_status, create_order, modify_order_status
from pyPOS.utils.entry      import get_entry_by_status, modify_entry_status
from pyPOS.utils.decorators import user_domain_required, credentials_level_required

bp = Blueprint( 'order', __name__, url_prefix='/order' )

@bp.route( '/' )
@credentials_level_required( [ 'admin', 'user' ] )
def index():
    id = None
    if g.user[ 'position' ] == 'user': id = g.user[ 'id' ]
    return render_template( 'order/index.html', order_dict=get_order_by_status( id ) )

@bp.route( '/add', methods=[ 'GET', 'POST' ] )
@credentials_level_required( [ 'admin', 'user' ] )
def add():
    if request.method == 'POST':
        name = request.form[ 'name' ]
        id = g.user[ 'id' ]
        create_order( name, id )
        return redirect( url_for( 'order.index' ) )
    return render_template( 'order/add.html' )

@bp.route( '/cancel/<int:id>' )
@credentials_level_required( [ 'admin', 'user' ] )
@user_domain_required( ['Open'] )
def cancel( id ):
    modify_order_status( id, 'Canceled' )
    modify_entry_status( id, 'Canceled', order=True )
    return redirect( url_for( 'order.index' ) )

@bp.route( '/open/<int:id>' )
@credentials_level_required( [ 'admin', 'user' ] )
@user_domain_required( ['Canceled'] )
def open( id ):
    modify_order_status( id, 'Open' )
    return redirect( url_for( 'order.index' ) )

@bp.route( '/review/<int:id>' )
@credentials_level_required( [ 'admin', 'user' ] )
@user_domain_required( ['Canceled', 'Complete'] )
def review( id ):
    return render_template( 'order/review.html', order_id=id, entry_dict=get_entry_by_status( id ) ) 

@bp.route( '/modify/<int:id>' )
@credentials_level_required( [ 'admin', 'user' ] )
@user_domain_required( ['Open'] )
def modify( id ):
    return render_template( 'order/modify.html', order_id=id, entry_dict=get_entry_by_status( id ) ) 
    