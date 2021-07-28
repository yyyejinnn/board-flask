from werkzeug.utils import redirect
from flask import Blueprint, url_for

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')  # 메인 화면
def index():
    return redirect(url_for('question._list'))
