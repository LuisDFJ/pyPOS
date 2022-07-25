from flask import Blueprint, redirect, url_for, render_template, request
from pyPOS.utils.admin import get_products

bp = Blueprint( 'admin-products', __name__, url_prefix='/admin/products' )

@bp.route( '/' )
def index():
    return render_template( 'admin/products/index.html', products=get_products() )

@bp.route( '/add/<int:id>', methods=( 'GET', 'POST' ) )
def add( id ):
    if request.method == 'POST':
        return redirect( url_for( 'admin-products.index' ) )
    return render_template( 'admin/products/add.html' )

@bp.route( '/modify/<int:id>', methods=( 'GET', 'POST' ) )
def modify( id ):

    if request.method == 'POST':
        return redirect( url_for( 'admin-products.index' ) )
    return render_template( 'admin/products/modify.html' )

@bp.route( '/delete/<int:id>', methods=( 'GET', 'POST' ) )
def delete( id ):
    if request.method == 'POST':
        return redirect( url_for( 'admin-products.index' ) )
    return render_template( 'admin/products/delete.html' )