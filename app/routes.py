import os
import uuid
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app, session
)
from werkzeug.utils import secure_filename

from app.utils import db_utils
from app.models.resume_processor import ResumeProcessor
from app.models.job_matcher import JobMatcher

bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/')
def index():
    return render_template('index.html')

# add a route for the home page
@bp.route('/home')
def home():
    return redirect(url_for('main.index')) # this is a placeholder

@bp.route('/upload_resume', methods=('GET', 'POST'))
def upload_resume():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'resume' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['resume']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Generate unique filename to prevent overwrites
            unique_filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Process resume
            resume_processor = ResumeProcessor(file_path)
            resume_text = resume_processor.extract_text()
            resume_features = resume_processor.extract_features()
            
            # Store in session for use on next page
            session['resume_text'] = resume_text
            session['resume_features'] = resume_features
            session['resume_path'] = file_path
            
            # Match with jobs
            job_matcher = JobMatcher()
            job_matches = job_matcher.find_matches(resume_text, resume_features)
            
            # Store match results in session
            session['job_matches'] = job_matches
            
            return redirect(url_for('main.dashboard'))
            
        else:
            flash('File type not allowed. Please upload PDF or DOCX.')
            return redirect(request.url)
            
    # GET request - show the upload form
    return render_template('upload_resume.html')

@bp.route('/dashboard')
def dashboard():
    # Retrieve saved job matches from session
    job_matches = session.get('job_matches', [])
    resume_features = session.get('resume_features', {})
    
    if not job_matches:
        flash('Please upload your resume first')
        return redirect(url_for('main.upload_resume'))
        
    return render_template('dashboard.html', job_matches=job_matches, resume_features=resume_features)

@bp.route('/job/<int:job_id>')
def job_detail(job_id):
    db = db_utils.get_db()
    job = db.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    
    if job is None:
        flash('Job not found')
        return redirect(url_for('main.dashboard'))
        
    # Get resume features from session if available
    resume_features = session.get('resume_features', {})
    
    return render_template('job_detail.html', job=job, resume_features=resume_features)

@bp.route('/admin/upload_jobs', methods=('GET', 'POST'))
def upload_jobs():
    # A simple admin interface for manually adding job listings
    # In a real app, you'd want proper authentication here
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        location = request.form['location']
        skills_required = request.form['skills_required']
        
        # Basic validation
        error = None
        if not title:
            error = 'Title is required'
        elif not description:
            error = 'Description is required'
            
        if error is not None:
            flash(error)
        else:
            db = db_utils.get_db()
            db.execute(
                'INSERT INTO jobs (title, company, description, location, skills_required)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, company, description, location, skills_required)
            )
            db.commit()
            flash('Job added successfully!')
            return redirect(url_for('main.upload_jobs'))
            
    # Get a list of existing jobs to display
    db = db_utils.get_db()
    jobs = db.execute('SELECT id, title, company FROM jobs ORDER BY id DESC').fetchall()
    return render_template('admin/upload_jobs.html', jobs=jobs)