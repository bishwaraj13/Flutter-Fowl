from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Leaderboard
from datetime import datetime, timedelta

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-score')
def submit_score():
    score = request.args.get('score', type=int)
    return render_template('submit_score.html', score=score)
    
@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    page = request.args.get('page', 1, type=int)
    time_filter = request.args.get('time_filter', 'all', type=str)
    
    # Time filtering logic...
    now = datetime.utcnow()
    if time_filter == 'daily':
        start_date = now - timedelta(days=1)
    elif time_filter == 'weekly':
        start_date = now - timedelta(weeks=1)
    else:
        start_date = datetime.min
    
    query = Leaderboard.query.filter(Leaderboard.timestamp >= start_date)
    
    if request.method == 'POST':
        if 'name' not in request.form or 'score' not in request.form:
            flash('Error: Please fill in all fields.')
            return redirect(url_for('submit_score', score=request.form['score']))
        
        name = request.form['name']
        score = request.form['score']
        
        if not name or not score:
            flash('Error: Please fill in all fields.')
            return redirect(url_for('submit_score', score=score))
        
        try:
            entry = Leaderboard(name=name, score=score)
            db.session.add(entry)
            db.session.commit()
            flash('Score submitted successfully.')
            return redirect(url_for('leaderboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error submitting score. Please try again.')
            return redirect(url_for('submit_score', score=score))
    else:
        scores = query.order_by(Leaderboard.score.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        return render_template('leaderboard.html', 
                             scores=scores,
                             time_filter=time_filter)