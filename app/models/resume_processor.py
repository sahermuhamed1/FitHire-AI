import re
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from app.utils.text_extractor import extract_text

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Try to load spacy model, fall back to smaller one if needed
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

class ResumeProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = None
        self.skills = []
        self.education = []
        self.experience = {}
        
    def extract_text(self):
        """Extract text from resume file"""
        self.text = extract_text(self.file_path)
        # Preprocess text (lowercase, remove extra whitespace)
        if self.text:
            self.text = self.preprocess_text(self.text)
        return self.text
    
    def preprocess_text(self, text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters (but keep some meaningful punctuation)
        text = re.sub(r'[^\w\s.,;:()-]', '', text)
        return text
    
    def remove_stopwords(self, text):
        """Remove common stopwords from text"""
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_text = [w for w in word_tokens if not w in stop_words]
        return ' '.join(filtered_text)
    
    def extract_skills(self):
        """Extract potential skills from resume text"""
        # Common programming languages and technologies
        common_skills = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php',
            'html', 'css', 'sql', 'nosql', 'react', 'angular', 'vue', 'node', 'express',
            'django', 'flask', 'spring', 'asp.net', 'jquery', 'bootstrap', 'tailwind',
            'mongodb', 'mysql', 'postgresql', 'oracle', 'aws', 'azure', 'gcp', 'docker',
            'kubernetes', 'jenkins', 'git', 'github', 'gitlab', 'jira', 'agile', 'scrum',
            'machine learning', 'artificial intelligence', 'data science', 'nlp', 'neural networks',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'tableau',
            'power bi', 'excel', 'word', 'powerpoint', 'photoshop', 'illustrator', 'figma',
            'ui/ux', 'mobile development', 'ios', 'android', 'react native', 'flutter', 'swift',
            'kotlin', 'objective-c', 'devops', 'ci/cd', 'linux', 'windows', 'macos', 'unix',
            'rest api', 'graphql', 'soap', 'microservices', 'testing', 'junit', 'selenium',
            'cypress', 'jest', 'mocha', 'chai'
        ]
        
        # Look for skills in resume text
        skills = []
        if self.text:
            for skill in common_skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', self.text, re.IGNORECASE):
                    skills.append(skill)
                    
        self.skills = skills
        return skills
    
    def extract_education(self):
        """Extract education information from resume"""
        education = []
        if self.text:
            # Look for common degree patterns
            degree_patterns = [
                r'\b(B\.?S\.?|Bachelor of Science|Bachelor\'?s?)\b',
                r'\b(B\.?A\.?|Bachelor of Arts)\b',
                r'\b(M\.?S\.?|Master of Science|Master\'?s?)\b',
                r'\b(M\.?B\.?A\.?|Master of Business Administration)\b',
                r'\b(Ph\.?D\.?|Doctor of Philosophy|Doctorate)\b'
            ]
            
            for pattern in degree_patterns:
                matches = re.findall(pattern, self.text, re.IGNORECASE)
                education.extend(matches)
                
        self.education = education
        return education
    
    def extract_years_of_experience(self):
        """Attempt to estimate years of experience"""
        if not self.text:
            return 0
            
        # Look for patterns like "X years of experience" or "X+ years"
        experience_patterns = [
            r'(\d+)\+?\s+years?\s+(?:of\s+)?experience',
            r'experience\s+(?:of\s+)?(\d+)\+?\s+years?'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE)
            if matches:
                # Return the highest number of years mentioned
                return max([int(y) for y in matches])
                
        return 0
    
    def extract_features(self):
        """Extract all features from resume text"""
        if not self.text:
            self.extract_text()
            
        features = {
            'skills': self.extract_skills(),
            'education': self.extract_education(),
            'years_of_experience': self.extract_years_of_experience()
        }
        
        return features