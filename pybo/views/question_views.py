from flask import Blueprint, render_template
from models import Question

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)  # 404 오류시 에러페이지 출력
    return render_template('question/question_detail.html', question=question)


@bp.route('/list/')  # 메인 화면
def _list():
    question_list = Question.query.order_by(
        Question.create_date.desc())  # 날짜별 정렬
    return render_template('question/question_list.html', question_list=question_list)
