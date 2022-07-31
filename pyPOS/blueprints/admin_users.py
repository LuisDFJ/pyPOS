from flask import Blueprint, render_template
from pyPOS.utils.admin import get_users
from pyPOS.utils.decorators import credentials_required_admin

bp = Blueprint( 'admin-users', __name__, url_prefix='/admin/users' )

@bp.route( '/' )
@credentials_required_admin
def index():
    users = get_users()
    return render_template( 'admin/users/index.html', users=users )