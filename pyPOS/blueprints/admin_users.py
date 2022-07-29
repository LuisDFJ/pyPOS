from flask import Blueprint, render_template, url_for

bp = Blueprint( 'admin-users', __name__, url_prefix='/admin/users' )

@bp.route( '/' )
def index():
    users = ['Luis', 'Diego']
    return render_template( 'admin/users/index.html', users=users )