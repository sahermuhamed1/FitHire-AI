# FitHire AI

An AI powered job matching platform that helps you find relevant job positions by analyzing resumes and matching the data in it with existing jobs from various job sources.

## 💫Features

- **AI Resume Analysis**: Extract skills, education, and experience from PDF/DOCX resumes
- **Smart Job Matching**: TF-IDF based matching algorithm for accurate job recommendations
- **Multi-Source Job Scraping**: Integrated scrapers for LinkedIn and other job site (will be implemented in the future)
- **Manual Profile Entry**: Option to manually input professional details instead of upload the resume
- **Simple Interface**: Clean Bootstrap-based UI with mobile responsiveness
- **Privacy Focused**: Local processing with no third-party data sharing

## ✅Technology Stack

- **Backend**: Python 3.8+, Flask 2.0.1
- **Database**: SQLite3
- **NLP/ML**: scikit-learn, NLTK, spaCy
- **Frontend**: Bootstrap 5, Jinja2
- **Job Scraping**: Selenium, BeautifulSoup4
- **Text Processing**: pdfminer.six, docx2txt

## 👾Project Structure

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


## 🧐Usage

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



## 🧑‍💻Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/feature-name`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/feature-name`)
5. Create Pull Request


# 🛜FitHire AI - Setup Guide

## Prerequisites
1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
2. Make sure Docker is running on your system

## Setup Steps

### 1️⃣Option 1: Using docker-compose (Recommended)

1. Clone the repository or copy the project files to your local machine
2. Open a terminal in the project directory
3. Run the following command:
```bash
docker-compose up -d 
```
4. The application will be available at http://localhost:8000

### 2️⃣Option 2: Using Docker directly

1. Clone the repository or copy the project files
2. Build the Docker image:
```bash
docker build -t fithire-ai .
```
3. Run the container:
```bash
docker run -d -p 8000:8000 \
  -v ./instance:/app/instance \
  -v ./logs:/app/logs \
  -v ./uploads:/app/uploads \
  --name fithire-ai \
  fithire-ai
```
4. Access the application at http://localhost:8000

## Stopping the Application

### For docker-compose:
```bash
docker-compose down
```

### For Docker:
```bash
docker stop fithire-ai
docker rm fithire-ai
```

## Viewing Logs

### For docker-compose:
```bash
docker-compose logs -f
```

### For Docker:
```bash
docker logs -f fithire-ai
```

## ⚠️Common Issues

1. **Port already in use**: If port 8000 is already being used by another app, modify the port mapping in docker-compose.yml or the docker run command to use a different port (e.g., 8001:8000)

2. **Permission issues**: Ensure Docker has permissions to access the mounted volumes. You may need to run commands with sudo on Linux.

3. **Docker not running**: Make sure Docker Desktop is running before executing any Docker commands.

## 📶Directory Structure
The following directories will be created and mounted into the container:
- `instance/`: Contains the SQLite database
- `logs/`: Application logs
- `uploads/`: Uploaded resume files

Make sure these directories exist and have proper write permissions.