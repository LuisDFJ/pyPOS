import os
import qrcode
import socket
import pyPOS
from dotenv import load_dotenv
from os.path import abspath, join, dirname

def generate_qr( username:str = "", token:str = "" ):
    out_path = join( dirname( abspath( pyPOS.__file__ ) ), r'static\users' )
    try:
        os.makedirs( out_path )
    except OSError:
        pass
    
    ip_addr     = socket.gethostbyname( socket.gethostname() )
    port        = os.getenv( 'FLASK_RUN_PORT' )
    login_addr  = f"http://{ip_addr}:{port}/auth/login?username={username}&password={token}"
    img         = qrcode.make( login_addr )
    img.save( f'{out_path}//{username}.png' )
