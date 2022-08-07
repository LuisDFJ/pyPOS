import functools
from flask import g, redirect, url_for
from pyPOS.utils.order import get_order
from pyPOS.utils.entry import get_entry

def entry_status_required( status:list ):
    def entry_status_required_wrap( view ):
        @functools.wraps( view )
        def wrapper_view( id, product_id, **kwargs ):
            entry = get_entry( product_id )
            if entry:
                if entry['status'].lower() in [ s.lower() for s in status ]:
                    return view( id, product_id, **kwargs )
            return redirect( url_for( 'index.index' ) )
        return wrapper_view
    return entry_status_required_wrap

def user_domain_required( status:list, levels:list = [ 'admin' ] ):
    def user_domain_required_wrap( view ):
        @functools.wraps( view )
        def wrapper_view( id, **kwargs ):
            order = get_order( id )
            if order:
                if g.user['position'] in levels or g.user['id'] == order['user_id']:
                    if order['status'].lower() in [ s.lower() for s in status ]:
                        return view( id, **kwargs )
            return redirect( url_for( 'index.index' ) )
        return wrapper_view
    return user_domain_required_wrap

def credentials_required( view ):
    @functools.wraps( view )
    def wrapped_view( **kwargs ):
        if g.user:
            return view( **kwargs )
        return redirect( url_for( 'auth.login' ) )
    return wrapped_view

def credentials_level_required( levels:list ):
    def credentials_level_required_wrap( view ):
        @functools.wraps( view )
        def wrapped_view( **kwargs ):
            if g.user:
                if g.user['position'] in levels:
                    return view( **kwargs )
                else:
                    return redirect( url_for( 'index.index' ) )        
            return redirect( url_for( 'auth.login' ) )
        return wrapped_view
    return credentials_level_required_wrap

def credentials_not_required( view ):
    @functools.wraps( view )
    def wrapped_view( **kwargs ):
        if g.user:
            return redirect( url_for( 'index.index' ) )
        return view( **kwargs )
    return wrapped_view