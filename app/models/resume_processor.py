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

# Initialize spaCy with better error handling
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    try:
        import subprocess
        result = subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        nlp = spacy.load("en_core_web_sm")
    except Exception as e:
        print(f"Error installing spaCy model: {e}")
        print("Please run: python -m spacy download en_core_web_sm")
        # Fallback to basic processing if spaCy fails
        nlp = None

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
        
    def evaluate_resume(self):
        """Evaluate resume quality as poor, good, very good, or excellent"""
        if not self.text:
            self.extract_text()
            
        if not self.skills:
            self.extract_skills()
            
        if not self.education:
            self.extract_education()
            
        # Calculate a basic score based on resume features
        score = 0
        
        # Score based on skills
        skill_count = len(self.skills)
        if skill_count >= 10:
            score += 3  # Excellent skills section
        elif skill_count >= 6:
            score += 2  # Very good skills section
        elif skill_count >= 3:
            score += 1  # Good skills section
        # else Poor skills section (0 points)
        
        # Score based on education
        if self.education:
            advanced_degrees = ['master', 'ph', 'phd', 'doctor', 'mba']
            has_advanced = any(any(adv in str(edu).lower() for adv in advanced_degrees) for edu in self.education)
            if has_advanced:
                score += 2  # Advanced degree
            else:
                score += 1  # Has education listed
        
        # Score based on experience
        years = self.extract_years_of_experience()
        if years >= 5:
            score += 3  # Significant experience
        elif years >= 3:
            score += 2  # Good experience
        elif years >= 1:
            score += 1  # Some experience
        
        # Score based on resume length/detail (using text length as a proxy)
        text_length = len(self.text) if self.text else 0
        if text_length >= 2000:
            score += 2  # Detailed resume
        elif text_length >= 1000:
            score += 1  # Adequate detail
        
        # Map score to rating
        if score >= 8:
            return "excellent"
        elif score >= 6:
            return "very good"
        elif score >= 3:
            return "good"
        else:
            return "poor"