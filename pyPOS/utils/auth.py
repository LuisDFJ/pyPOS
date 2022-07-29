import click
import secrets
import os
from flask import current_app, session
from flask.cli import with_appcontext
from pyPOS.utils.db import getDB, openSQL
from pyPOS.utils.qrcode import generate_qr
from pyPOS.utils.click_utils import ClickFlagRequired
from werkzeug.security import check_password_hash, generate_password_hash

def insert_into_user( username, position ):
    db = getDB()
    try:
        db.execute( 
            openSQL( 'insert_user.sql' ),
            ( username, position )
        )
        db.commit()
    except db.IntegrityError:
        click.echo( f'Registration Fail: User already exists.' )
        return False
    else:
        click.echo( f'User created: [{position}]:{username}' )
    return True

def insert_into_credentials( file, username, password, position ):
    db = getDB()
    try:
        db.execute( 
            openSQL( file ),
            ( username, password )
        )
        db.commit()
    except db.IntegrityError:
        click.echo( f'Registration Fail: Credentials missing.' )
    else:
        click.echo( f'Credentials added: [{position}]:{username}' )

def user_authentication( username, password ):
    db = getDB()
    user = db.execute(
        'SELECT position FROM user WHERE username = ?',
        ( username, )
    ).fetchone()
    if user:
        position = user[ 'position' ]
        if position == 'admin':
            user = db.execute(
                openSQL( 'fetch_credential_admin.sql' ),
                ( username, )
            ).fetchone()
            return check_password_hash( user['password'], password ), user['id']
        elif position == 'user':
            user = db.execute(
                openSQL( 'fetch_credential_user.sql' ),
                ( username, )
            ).fetchone()
            return user['password'] == password, user['id']
    return False, None

def authenticate( username, password ):
    error = None
    if username and password:
        flag, id = user_authentication( username, password )
        if flag:
            session.clear()
            session[ 'user_id' ] = id
        else:
            error = 'Error: Incorrect credentials.'
    else:
        error = 'Error: Faulty submition.'
    return error

def roll_up_secret():
    config_path = os.path.join( current_app.instance_path, 'config.py' )
    try:
        os.makedirs( current_app.instance_path )
    except OSError:
        pass
    with open( config_path, 'a+' ) as pFile: pass
    with open( config_path, 'r' )  as pFile: lines = pFile.readlines()
    found = False
    for i, line in enumerate( lines ):
        if 'SECRET_KEY' in line:
            found = True
            lines[i] = f'SECRET_KEY = "{secrets.token_hex()}"\n'
            break
    if not found:
        lines.append( f'\nSECRET_KEY = "{secrets.token_hex()}"' )
    with open( config_path, 'w' ) as pFile: pFile.writelines( lines )

@click.command( 'create-user' )
@click.option( '--admin', is_flag=True, is_eager=False )
@click.option( '--username', prompt=True )
@click.option( '--password', prompt=True, hide_input=True, confirmation_prompt=True, cls=ClickFlagRequired, flag_required='admin' )
@with_appcontext
def create_user_command( admin, username, password ):
    if admin:
        if insert_into_user( username, 'admin' ):
            insert_into_credentials( 'insert_credential_admin.sql', username, generate_password_hash( password ), 'admin' )
    else:
        if insert_into_user( username, 'user' ):
            insert_into_credentials( 'insert_credential_user.sql', username, 'null', 'user' )

@click.command( 'delete-user' )
@click.option( '--username', prompt=True )
@with_appcontext
def delete_user_command( username ):
    db = getDB()
    user = db.execute(
        'SELECT id, position FROM user WHERE username = ?',
        ( username, )
    ).fetchone()
    if user:
        db.execute( f'DELETE FROM user_{ user["position"] } WHERE user_id = ?', ( user['id'], ) )
        db.execute( 'DELETE FROM user WHERE id = ?', ( user['id'], ) )
        db.commit()
    else:
        click.echo( f'Not existing user [{username}]' )

@click.command( 'gen-tokens' )
@with_appcontext
def gen_tokens_command():
    db = getDB()
    users = db.execute(
        'SELECT id FROM user_user'
    ).fetchall()
    for user in users:
        db.execute(
            'UPDATE user_user SET password = ? WHERE id = ?',
            ( secrets.token_hex( current_app.config['TOKEN_LENGTH'] ), user['id'] )
        )
    db.commit()
    roll_up_secret()
    click.echo( 'Tokens updated' )
    
    users = db.execute(
        openSQL( 'fetch_users.sql' )
    ).fetchall()
    for user in users:
        generate_qr( user['username'],user['password'] )
    click.echo( 'QR codes updated' )