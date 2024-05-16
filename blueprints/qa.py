from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models import Question, Answer
from exts import db
from .forms import PostQuestionForm, AnswerForm

bp = Blueprint('qa', __name__)

@bp.route('/')
def index():
    questions = Question.query.all()
    return render_template('index.html', questions=questions)

@bp.route('/post_question', methods=['GET', 'POST'])
@login_required
def post_question():
    form = PostQuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(question)
        db.session.commit()
        flash('Your question has been posted!', 'success')
        return redirect(url_for('qa.index'))
    return render_template('post_question.html', form=form)

@bp.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question_detail(question_id):
    question = Question.query.get_or_404(question_id)
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(content=form.content.data, author=current_user, question=question)
        db.session.add(answer)
        db.session.commit()
        flash('Your answer has been posted!', 'success')
        return redirect(url_for('qa.question_detail', question_id=question.id))
    return render_template('detail.html', question=question, form=form)
