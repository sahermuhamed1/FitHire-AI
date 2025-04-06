# AI Resume Matcher

A Flask-based web application that uses Natural Language Processing (NLP) to match resumes with job listings based on content similarity and skill matches.

## Features

- Upload resumes in PDF or DOCX format
- Extract text and key information using NLP techniques
- Identify skills, education, and years of experience
- Match resumes against job listings using TF-IDF and cosine similarity
- View job matches with similarity scores
- Admin interface for adding new job listings

## Project Structure

```
app/
├── templates/          # Jinja2 HTML templates
├── static/             # CSS, JS, and other static files
├── models/             # ML/NLP logic
├── utils/              # Parsing and database utilities
├── routes.py           # Flask routes
├── __init__.py         # App factory
├── schema.sql          # Database schema
instance/
├── ai_matcher.db       # SQLite database (created at runtime)
run.py                  # Application entry point
config.py               # Configuration settings
requirements.txt        # Dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/sahermuhamed1/FitHire-AI.git
   cd FitHire-AI
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Download required NLTK data and spaCy model:
   ```
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   python -m spacy download en_core_web_sm
   ```

5. Initialize the database:
   ```
   flask --app run init-db
   ```

## Running the Application

```
flask --app run run --debug
```

The application will be available at http://localhost:5000.

## Usage

1. Visit the home page and navigate to "Upload Resume"
2. Upload your resume in PDF or DOCX format
3. View the list of job matches on the dashboard
4. Click on any job to see more details

## Admin Interface

The admin interface is available at `/admin/upload_jobs` and allows:
- Adding new job listings
- Viewing existing job listings

## Future Enhancements

- User authentication system
- Resume feedback and improvement suggestions
- Job listing scraping functionality
- Automated job application system
- Enhanced matching algorithms using deep learning

## Technologies Used

- Flask (Python web framework)
- SQLite (Database)
- NLTK and spaCy (Natural Language Processing)
- scikit-learn (TF-IDF, cosine similarity)
- Bootstrap (Frontend framework)
- pdfminer.six and docx2txt (Document parsing)