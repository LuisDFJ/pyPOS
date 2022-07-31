import functools
from flask import g, redirect, url_for

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

