from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Icon keyword (e.g., 'code', 'layers', 'globe', 'database')
    
    questions = db.relationship('Question', backref='category', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'question_count': len(self.questions)
        }

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(50), nullable=False)  # 'Easy', 'Medium', 'Hard'

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'question_text': self.question_text,
            'options': {
                'A': self.option_a,
                'B': self.option_b,
                'C': self.option_c,
                'D': self.option_d
            },
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'difficulty': self.difficulty
        }

class Attempt(db.Model):
    __tablename__ = 'attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    category_name = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    time_taken = db.Column(db.Integer, nullable=False)  # Time taken in seconds
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationship to get individual answers for this attempt
    answers = db.relationship('AttemptAnswer', backref='attempt', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'category_name': self.category_name,
            'difficulty': self.difficulty,
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': round(self.percentage, 1),
            'time_taken': self.time_taken,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

class AttemptAnswer(db.Model):
    __tablename__ = 'attempt_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_answer = db.Column(db.String(1), nullable=True)  # 'A', 'B', 'C', 'D' or None (skipped)
    
    # Relationship to get the question details directly
    question = db.relationship('Question')

    def to_dict(self):
        return {
            'id': self.id,
            'attempt_id': self.attempt_id,
            'question_id': self.question_id,
            'selected_answer': self.selected_answer,
            'is_correct': self.selected_answer == self.question.correct_answer if self.question else False
        }
