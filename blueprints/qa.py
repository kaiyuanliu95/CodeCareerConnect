from flask import Blueprint, render_template
from models import QuestionModel, AnswerModel

# Create a Flask Blueprint named 'qa', which helps in organizing a group of related views and other code.
# The Blueprint is configured to handle routes at the base URL ('/').
bp = Blueprint("qa", __name__, url_prefix="/")

@bp.route("/")
def index():
    # Fetch all questions from the database, ordered by creation time in descending order.
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    # Render and return the 'index.html' template, passing the fetched questions for display.
    return render_template("index.html", questions=questions)

@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    # Fetch a specific question by its ID.
    question = QuestionModel.query.get(qa_id)
    # Render the 'detail.html' template, passing the fetched question for display.
    return render_template("detail.html", question=question)
