import re
import functools
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from app import db
from models import User
from forms import UserCreateForm, UserLoginForm


bp = Blueprint('auth', __name__, url_prefix="/auth")


@bp.before_app_request  # 모든 라우트 함수보다 앞에 실행
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/signup/', methods=('POST', 'GET'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data, password=generate_password_hash(
                form.password1.data), email=form.email.data)
            # generate_password_hash : 암호화 후 저장
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('POST', 'GET'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."

        if error is None:  # 로그인 문제 없으면
            session.clear()
            session['user_id'] = user.id  # 세션값 저장
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html', form=form)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):  # 데코 함수 생성
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:  # 로그인 유저 없으면 로그인 페이지 반환
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
