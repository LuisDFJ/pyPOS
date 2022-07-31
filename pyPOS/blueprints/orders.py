from tkinter.messagebox import RETRY
from flask import Blueprint, render_template
from pyPOS.utils.admin import get_products

bp = Blueprint( 'order', __name__, url_prefix='/order' )

@bp.route( '/' )
def index():
    return render_template( 'order/index.html', products=get_products() )