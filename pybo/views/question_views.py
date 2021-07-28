from flask import Blueprint, render_template, request, g, flash
from flask.helpers import url_for
from werkzeug.utils import redirect
from models import Question
from forms import QuestionForm, AnswerForm
from datetime import datetime
from app import db
from views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():  # 정합성 검사 / 실패 시 False 반환
        question = Question(subject=form.subject.data,
                            content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)  # 404 오류시 에러페이지 출력
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/list/')  # 메인 화면
def _list():
    page = request.args.get('page', type=int, default=1)  # paging
    question_list = Question.query.order_by(
        Question.create_date.desc())  # 날짜별 정렬
    question_list = question_list.paginate(page, per_page=10)  # paging
    return render_template('question/question_list.html', question_list=question_list)


# 수정
@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)

    if g.user != question.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))

    if request.method == "POST":  # 저장하기 눌렀을 때
        form = QuestionForm()
        if form.validate_on_submit():  # Question Form 검증
            form.populate_obj(question)  # form에 입력되어 있는데이터를 question 객체에 적용
            question.modify_date = datetime.now()  # 수정일자
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # get : 질문 수정 눌렀을 때
        form = QuestionForm(obj=question)
        return render_template('question/question_form.html', form=form)


# 삭제
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))

    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
