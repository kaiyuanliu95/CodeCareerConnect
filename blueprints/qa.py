from flask import Blueprint, redirect, url_for, request, render_template, g
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts  import db
from decorators import  login_required

# from decorators import  login_required
bp = Blueprint("qa",__name__, url_prefix="/")

# Route for the homepage that displays a list of questions
@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html",questions = questions)

# Route for posting a new question, requires user to be logged in
@bp.route("/post_question",methods=['GET','POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html") # Render question posting form if GET request
    else:
        form = QuestionForm(request.form) # Initialize form with POST data
        if form.validate(): # Validate form
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user) # Create a new question
            db.session.add(question) # Add question to the database
            db.session.commit()
            # TODO:
            return redirect("/") # Redirect to homepage
        else:
            print(form.errors) # Print form errors
            return  redirect(url_for("qa.public")) # Redirect back to question posting page

# Route for displaying the details of a specific question
@bp.route("/qa/detail/<int:qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id) # Get question by ID
    return render_template("detail.html",question=question)

# Route for posting an answer to a question, requires user to be logged in
@bp.post("/answer/public")
@login_required
def public_answer():
    form = AnswerForm(request.form) # Initialize form with POST data
    if form.validate(): # Validate form
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content,question_id=question_id,author_id=g.user.id) # Create a new answer
        db.session.add(answer) # Add answer to the database
        db.session.commit()
        return redirect(url_for("qa.qa_detail",qa_id=question_id)) # Redirect to question details page
    else:
        print(form.errors) # Print form errors
        return redirect(url_for("qa.qa_detail",qa_id=request.form.get("question_id"))) # Redirect back to question details page
    
# Route for searching questions by title
@bp.route("/search")
def search():
    q = request.args.get("q") # Get search query from URL parameters
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all() # Filter questions by title
    return render_template("index.html",questions=questions)


