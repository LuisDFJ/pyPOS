from ast import arg
from operator import mod
import pyPOS
from flask import Blueprint, flash, redirect, url_for, render_template, request
from os.path import dirname, abspath, join
from werkzeug.utils import secure_filename
from pyPOS.utils.admin import get_products, CATEGORIES, allowed_file, add_product, delete_product, get_product, modify_product
from pyPOS.utils.decorators import credentials_required_admin

bp = Blueprint( 'admin-products', __name__, url_prefix='/admin/products' )

@bp.route( '/' )
@credentials_required_admin
def index():
    return render_template( 'admin/products/index.html', products=get_products() )

@bp.route( '/add', methods=( 'GET', 'POST' ) )
@credentials_required_admin
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
                args[ 'price' ]     = float( args['price'] )
                error = add_product( **args )
                if not error:
                    return redirect( url_for( 'admin-products.index' ) )
        flash( error )
        return redirect( request.url )
    return render_template( 'admin/products/add.html', categories=CATEGORIES )

@bp.route( '/modify/<int:id>', methods=( 'GET', 'POST' ) )
@credentials_required_admin
def modify( id ):
    if request.method == 'POST':
        args = dict( request.form )
        args[ 'price' ]     = float( args['price'] )
        modify_product( id, **args )
        return redirect( url_for( 'admin-products.index' ) )
    product = dict( get_product( id ) )
    return render_template( 'admin/products/modify.html', **product )

@bp.route( '/delete/<int:id>' )
@credentials_required_admin
def delete( id ):
    delete_product( id )
    return redirect( url_for( 'admin-products.index' ) )