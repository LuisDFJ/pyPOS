from flask import Blueprint, flash, redirect, url_for, render_template, request
from pyPOS.utils.admin import get_products, CATEGORIES, allowed_file, add_product
from werkzeug.utils import secure_filename
from os.path import dirname, abspath, join
import pyPOS

bp = Blueprint( 'admin-products', __name__, url_prefix='/admin/products' )

@bp.route( '/' )
def index():
    return render_template( 'admin/products/index.html', products=get_products() )

@bp.route( '/add', methods=( 'GET', 'POST' ) )
def add():
    if request.method == 'POST':
        error = 'No file part.'
        if 'thumbnail' in request.files:
            file = request.files[ 'thumbnail' ]
            if file.filename and file and allowed_file( file.filename ):
                filename = secure_filename( file.filename )
                out_path = join( dirname( abspath( pyPOS.__file__ ) ), f'static/products/{filename}' )
                file.save( out_path )
                args = dict( request.form )
                args[ 'thumbnail' ] = filename
                error = add_product( **args )
                if not error:
                    return redirect( url_for( 'admin-products.index' ) )
        flash( error )
        return redirect( request.url )
    return render_template( 'admin/products/add.html', categories=CATEGORIES )

@bp.route( '/modify/<int:id>', methods=( 'GET', 'POST' ) )
def modify( id ):
    if request.method == 'POST':
        return redirect( url_for( 'admin-products.index' ) )
    return render_template( 'admin/products/modify.html' )

@bp.route( '/delete/<int:id>' )
def delete( id ):
    print( f'Delete item: {id}' )
    return redirect( url_for( 'admin-products.index' ) )