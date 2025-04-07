# FitHire AI

An AI-powered job matching platform that helps job seekers find relevant positions by analyzing resumes and matching them with job listings from various sources including LinkedIn.

## Features

- **AI Resume Analysis**: Extract skills, education, and experience from PDF/DOCX resumes
- **Smart Job Matching**: TF-IDF based matching algorithm for accurate job recommendations
- **Multi-Source Job Scraping**: Integrated scrapers for LinkedIn and other job sites
- **Manual Profile Entry**: Option to manually input professional details
- **Simple Interface**: Clean Bootstrap-based UI with mobile responsiveness
- **Privacy Focused**: Local processing with no third-party data sharing

## Technology Stack

- **Backend**: Python 3.8+, Flask 2.0.1
- **Database**: SQLite3
- **NLP/ML**: scikit-learn, NLTK, spaCy
- **Frontend**: Bootstrap 5, Jinja2
- **Job Scraping**: Selenium, BeautifulSoup4
- **Text Processing**: pdfminer.six, docx2txt

## Project Structure

```
FitHire-AI/
├── app/
│   ├── models/
│   │   ├── job_matcher.py
│   │   ├── manual_processor.py
│   │   └── resume_processor.py
│   ├── static/
│   │   ├── css/
│   │   └── site.webmanifest
│   ├── templates/
│   │   ├── admin/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── ...
│   ├── utils/
│   │   ├── base_scraper.py
│   │   ├── db_utils.py
│   │   ├── job_scraper.py
│   │   └── linkedin_scraper.py
│   ├── routes.py
│   └── schema.sql
├── config/
│   └── __init__.py
├── scripts/
│   └── scrape_jobs.py
├── tests/
│   └── conftest.py
├── .env.example
├── .gitignore
├── requirements.txt
└── run.py
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd FitHire-AI
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/macOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Initialize database:
```bash
flask init-db
```

6. Run the application:
```bash
python run.py
```

## Usage

1. **Resume Upload**:
   - Navigate to Upload Resume page
   - Select PDF or DOCX resume file
   - System will analyze and extract information

2. **Manual Entry**:
   - Use Manual Entry page for direct input
   - Enter skills, education, and experience
   - System will create a profile for matching

3. **View Matches**:
   - System displays matching jobs
   - Results ranked by relevance
   - Click job listings for details

## Development

### Setup Development Environment

```bash
# Install dev dependencies
pip install -r requirements.txt

# Initialize database
flask init-db

# Run development server
flask run --debug
```

### Running Tests

```bash
pytest
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/feature-name`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/feature-name`)
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.