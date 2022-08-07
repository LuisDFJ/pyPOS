from flask import Blueprint, render_template
from pyPOS.utils.admin import get_users
from pyPOS.utils.decorators import credentials_level_required

bp = Blueprint( 'admin-users', __name__, url_prefix='/admin/users' )

@bp.route( '/' )
@credentials_level_required( 'admin' )
def index():
    users = get_users()
    return render_template( 'admin/users/index.html', users=users )