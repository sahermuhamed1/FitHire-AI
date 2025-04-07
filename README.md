# FitHire AI

An AI-powered job matching platform that helps job seekers find relevant positions by analyzing their resumes.

## Project Structure

```
FitHire-AI/
├── app/                  # Application package
│   ├── models/          # Data models and business logic
│   ├── routes/          # Route handlers
│   ├── static/          # Static files (CSS, JS, images)
│   ├── templates/       # Jinja2 templates
│   └── utils/           # Utility functions and helpers
├── config/              # Configuration files
├── docs/                # Documentation
├── scripts/             # Utility scripts
├── tests/               # Test suite
└── requirements.txt     # Project dependencies
```

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/macOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure
6. Run the application: `python run.py`

## Development

- Run tests: `pytest`
- Run linter: `flake8`
- Format code: `black .`

## License

MIT License
