import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.db_utils import get_db

import pandas as pd

class JobMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def preprocess_for_matching(self, text):
        """Prepare text for TF-IDF vectorization"""
        # Basic preprocessing is already done in ResumeProcessor
        return text
        
    def find_matches(self, resume_text, resume_features=None, top_n=10):
        """Find matching jobs based on resume text and extracted features"""
        import logging
        logger = logging.getLogger(__name__)
        
        db = get_db()
        all_jobs = db.execute('SELECT * FROM jobs').fetchall()
        
        logger.debug(f"Found {len(all_jobs)} jobs in database")
        
        if not all_jobs:
            logger.warning("No jobs found in database")
            return []
            
        # Prepare corpus for TF-IDF (resume + all job descriptions)
        corpus = [self.preprocess_for_matching(resume_text)]
        job_ids = []
        
        for job in all_jobs:
            corpus.append(self.preprocess_for_matching(job['description']))
            job_ids.append(job['id'])
            
        # Calculate TF-IDF vectors
        try:
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
        except ValueError as e:
            print(f"Error in TF-IDF calculation: {e}")
            return []
        
        
                
        # Calculate cosine similarity between resume and all jobs
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
        # Enhanced scoring with skills matching if resume_features available
        if resume_features and 'skills' in resume_features and resume_features['skills']:
            resume_skills = set(skill.lower() for skill in resume_features['skills'])
            
            # Adjust scores based on skill matches
            for i, job in enumerate(all_jobs):
                if job['skills_required']:
                    job_skills = set(skill.strip().lower() for skill in job['skills_required'].split(','))
                    skill_matches = resume_skills.intersection(job_skills)
                    
                    # Boost score based on percentage of required skills matched
                    if job_skills:
                        skill_match_score = len(skill_matches) / len(job_skills)
                        # Weight: 70% TF-IDF similarity, 30% skill matching
                        cosine_similarities[i] = 0.7 * cosine_similarities[i] + 0.3 * skill_match_score
        
        # Create job entries with similarity scores
        job_matches = []
        for i, score in enumerate(cosine_similarities):
            job = dict(all_jobs[i])
            job['match_score'] = round(float(score * 100), 1)  # Convert to percentage
            job_matches.append(job)
            
        # Sort by match score (descending)
        job_matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Return top N matches
        logger.debug(f"Calculated {len(cosine_similarities)} similarity scores")
        logger.debug(f"Returning {len(job_matches[:top_n])} job matches")
        
        return job_matches[:top_n]
        
    def get_job_by_id(self, job_id):
        """Retrieve a specific job by ID"""
        db = get_db()
        job = db.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
        if job:
            return dict(job)
        return None