from flask                  import Blueprint, render_template, g, request, redirect, url_for
from pyPOS.utils.order      import get_order_by_status, create_order, modify_order_status, get_entries
from pyPOS.utils.decorators import credentials_required, user_domain_required

bp = Blueprint( 'order', __name__, url_prefix='/order' )

@bp.route( '/' )
@credentials_required
def index():
    id = None
    if g.user[ 'position' ] == 'user': id = g.user[ 'id' ]
    return render_template( 'order/index.html', order_dict=get_order_by_status( id ) )

@bp.route( '/add', methods=[ 'GET', 'POST' ] )
@credentials_required
def add():
    if request.method == 'POST':
        name = request.form[ 'name' ]
        id = g.user[ 'id' ]
        create_order( name, id )
        return redirect( url_for( 'order.index' ) )
    return render_template( 'order/add.html' )

@bp.route( '/cancel/<int:id>' )
@credentials_required
@user_domain_required( ['Open'] )
def cancel( id ):
    modify_order_status( id, 'Canceled' )
    return redirect( url_for( 'order.index' ) )

@bp.route( '/open/<int:id>' )
@credentials_required
@user_domain_required( ['Canceled'] )
def open( id ):
    modify_order_status( id, 'Open' )
    return redirect( url_for( 'order.index' ) )

@bp.route( '/review/<int:id>' )
@credentials_required
@user_domain_required( ['Canceled', 'Complete'] )
def review( id ):
    #modify_order_status( id, 'Canceled' )
    print( id )
    return redirect( url_for( 'order.index' ) )

@bp.route( '/modify/<int:id>' )
@credentials_required
@user_domain_required( ['Open'] )
def modify( id ):
    product_list = [
        { 'name': 'Food1', 'comment':'This is a comment', 'thumbnail':'food_thumbnail.jpg', 'price':12.5 },
        { 'name': 'Food2', 'comment':'This is a comment', 'thumbnail':'food_thumbnail.jpg', 'price':12.5 },
    ]
    entries = get_entries( id )
    print( [ dict( entry ) for entry in entries ] )
    return render_template( 'order/modify.html', order_id=id, product_list=entries ) 
    