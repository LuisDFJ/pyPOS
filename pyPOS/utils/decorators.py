import functools
from flask import g, redirect, url_for
from pyPOS.utils.order import get_order

def user_domain_required( status:list ):
    def user_domain_required_wrap( view ):
        @functools.wraps( view )
        def wrapper_view( id, **kwargs ):
            order = get_order( id )
            if order:
                if g.user['position'] == 'admin' or g.user['id'] == order['user_id']:
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
        
def credentials_required_admin( view ):
    @functools.wraps( view )
    def wrapped_view( **kwargs ):
        if g.user:
            if g.user['position'] == 'admin':
                return view( **kwargs )
            else:
                return redirect( url_for( 'index.index' ) )        
        return redirect( url_for( 'auth.login' ) )
    return wrapped_view

def credentials_not_required( view ):
    @functools.wraps( view )
    def wrapped_view( **kwargs ):
        if g.user:
            return redirect( url_for( 'index.index' ) )
        return view( **kwargs )
    return wrapped_view