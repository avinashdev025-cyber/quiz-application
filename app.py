import os
import random
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Category, Question, Attempt, AttemptAnswer
from questions_seed import seed_database

app = Flask(__name__)

# Resolve database file path dynamically inside the project directory
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'quiz.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-12345'

db.init_app(app)

# Ensure database creation and seeding run inside app context on startup
with app.app_context():
    db.create_all()
    if Category.query.count() == 0:
        seed_database()

# Inject active categories helper to avoid repeating queries in templates
@app.context_processor
def inject_categories():
    return dict(all_categories=Category.query.all())

# --- WEB PAGE ROUTES ---

@app.route('/')
def index():
    """Start page: Enter username, select category and difficulty."""
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@app.route('/quiz')
def quiz():
    """Quiz session UI. Requires name, category_id and difficulty query parameters."""
    user_name = request.args.get('user_name', '').strip()
    category_id = request.args.get('category_id')
    difficulty = request.args.get('difficulty', 'Easy')
    
    if not user_name or not category_id:
        return redirect(url_for('index'))
        
    category = Category.query.get_or_404(category_id)
    return render_template('quiz.html', user_name=user_name, category=category, difficulty=difficulty)

@app.route('/result/<int:attempt_id>')
def result(attempt_id):
    """Review screen for a finished quiz attempt."""
    attempt = Attempt.query.get_or_404(attempt_id)
    # Fetch questions and responses in original order by joining AttemptAnswer
    answers = AttemptAnswer.query.filter_by(attempt_id=attempt_id).all()
    return render_template('result.html', attempt=attempt, answers=answers)

@app.route('/leaderboard')
def leaderboard():
    """High score page displaying all quiz attempts sorted by percentage and speed."""
    # Order by score percent DESC, then time_taken ASC
    attempts = Attempt.query.order_by(Attempt.percentage.desc(), Attempt.time_taken.asc()).limit(50).all()
    return render_template('leaderboard.html', attempts=attempts)

@app.route('/admin')
def admin():
    """Manage database records and view stats."""
    categories = Category.query.all()
    questions = Question.query.all()
    attempts = Attempt.query.all()
    
    # Calculate some helper statistics
    total_attempts = len(attempts)
    avg_score = sum([a.percentage for a in attempts]) / total_attempts if total_attempts > 0 else 0.0
    
    # Category question distribution
    cat_stats = []
    for cat in categories:
        cat_stats.append({
            'name': cat.name,
            'count': len(cat.questions)
        })
        
    return render_template('admin.html', 
                           categories=categories, 
                           questions=questions, 
                           attempts=attempts,
                           total_attempts=total_attempts,
                           avg_score=round(avg_score, 1),
                           cat_stats=cat_stats)


# --- QUESTION CRUD ENDPOINTS (ADMIN ONLY) ---

@app.route('/admin/add-question', methods=['POST'])
def add_question():
    """Add a new question to the database."""
    category_id = request.form.get('category_id', type=int)
    question_text = request.form.get('question_text', '').strip()
    option_a = request.form.get('option_a', '').strip()
    option_b = request.form.get('option_b', '').strip()
    option_c = request.form.get('option_c', '').strip()
    option_d = request.form.get('option_d', '').strip()
    correct_answer = request.form.get('correct_answer', 'A')
    difficulty = request.form.get('difficulty', 'Easy')
    explanation = request.form.get('explanation', '').strip()
    
    if category_id and question_text and option_a and option_b and option_c and option_d:
        new_q = Question(
            category_id=category_id,
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            difficulty=difficulty,
            explanation=explanation
        )
        db.session.add(new_q)
        db.session.commit()
        
    return redirect(url_for('admin'))

@app.route('/admin/delete-question/<int:question_id>', methods=['POST', 'GET'])
def delete_question(question_id):
    """Delete a question from the database."""
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('admin'))


# --- JSON API ENDPOINTS ---

@app.route('/api/questions')
def get_questions():
    """
    Returns a JSON list of questions filtered by category and difficulty.
    Shuffled and limited to 10 questions.
    """
    category_id = request.args.get('category_id', type=int)
    difficulty = request.args.get('difficulty', '')
    
    query = Question.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    if difficulty and difficulty != 'all':
        query = query.filter_by(difficulty=difficulty)
        
    questions = query.all()
    
    # Shuffle and select a maximum of 10 questions
    random.shuffle(questions)
    selected_questions = questions[:10]
    
    return jsonify([q.to_dict() for q in selected_questions])

@app.route('/api/submit-attempt', methods=['POST'])
def submit_attempt():
    """
    Submit and grade a quiz attempt.
    Payload format:
    {
      "user_name": "Name",
      "category_id": 1,
      "difficulty": "Easy",
      "time_taken": 45,
      "answers": {
         "question_id_1": "B",
         "question_id_2": "A"
      }
    }
    """
    data = request.get_json() or {}
    
    user_name = data.get('user_name', 'Anonymous').strip() or 'Anonymous'
    category_id = data.get('category_id')
    difficulty = data.get('difficulty', 'Easy')
    time_taken = data.get('time_taken', 0)
    user_answers = data.get('answers', {})  # Map of { question_id_str: selected_choice_str }
    
    category = Category.query.get_or_404(category_id)
    
    # Retrieve all questions related to this attempt
    question_ids = [int(qid) for qid in user_answers.keys()]
    questions = Question.query.filter(Question.id.in_(question_ids)).all()
    
    score = 0
    total_questions = len(questions)
    
    # We will record attempt details and create answers
    # Wait, create the attempt first to get its ID
    attempt = Attempt(
        user_name=user_name,
        category_name=category.name,
        difficulty=difficulty,
        score=0,  # placeholder, will update below
        total_questions=total_questions,
        percentage=0.0,
        time_taken=time_taken
    )
    db.session.add(attempt)
    db.session.flush()  # Populates attempt.id without committing yet
    
    for q in questions:
        selected = user_answers.get(str(q.id))
        is_correct = (selected == q.correct_answer)
        if is_correct:
            score += 1
            
        ans = AttemptAnswer(
            attempt_id=attempt.id,
            question_id=q.id,
            selected_answer=selected
        )
        db.session.add(ans)
        
    # Calculate score percentage
    percentage = (score / total_questions * 100) if total_questions > 0 else 0.0
    
    # Update attempt score and percent
    attempt.score = score
    attempt.percentage = percentage
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'attempt_id': attempt.id,
        'score': score,
        'total_questions': total_questions,
        'percentage': round(percentage, 1)
    })

if __name__ == '__main__':
    # Launch local development server
    app.run(debug=True)
