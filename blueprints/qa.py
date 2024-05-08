from flask import Blueprint, render_template
from models import QuestionModel, AnswerModel
from flask import request, redirect, url_for, g
from .forms import QuestionForm, AnswerForm 
from exts import db
from decorators import login_required


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

@bp.route("/qa/publish", methods=['GET', 'POST'])
@login_required  # Use the custom decorator to require login for this route.
def publish_question():
    if request.method == 'GET':
        # If the request is a GET, render the form to publish a new question.
        return render_template("publish_question.html")
    else:
        # If the request is a POST, process the submitted form.
        form = QuestionForm(request.form)
        if form.validate():  # Validate the form data.
            title = form.title.data
            content = form.content.data
            # Create a new question instance using the validated data.
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)  # Add the new question to the session.
            db.session.commit()  # Commit the transaction to save the question to the database.
            # Redirect to the home page after successful submission.
            return redirect("/")
        else:
            # If validation fails, print errors and redirect back to the question form.
            print(form.errors)
            return redirect(url_for("qa.publish"))

@bp.post("/answer/publish")  # Use the new decorator '@bp.post' which specifies POST method only.
@login_required  # Require user login to access this route.
def publish_answer():
    form = AnswerForm(request.form)
    if form.validate():  # Validate the submitted form data.
        content = form.content.data
        question_id = form.question_id.data
        # Create a new answer instance using the validated data.
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)  # Add the new answer to the session.
        db.session.commit()  # Commit the transaction to save the answer to the database.
        # Redirect to the question detail page after successful submission.
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        # If validation fails, print errors and redirect back to the detail page of the current question.
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))
    
@bp.route("/search")
def search():
    # Retrieve the search query from the request's query string.
    q = request.args.get("q")
    # Perform a search in the database for questions that contain the search term in their title.
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    # Render the 'index.html' template, passing the search results for display.
    return render_template("index.html", questions=questions)

