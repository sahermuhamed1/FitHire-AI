import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.db_utils import get_db

import pandas as pd

class JobMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def preprocess_for_matching(self, text):
        # Basic preprocessing is already done in ResumeProcessor
        return text
        
    def find_matches(self, resume_text, resume_features=None, top_n=10):
        # Find matching jobs based on resume text and extracted features
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
        jobs_with_scores = []
        
        for job in all_jobs:
            corpus.append(self.preprocess_for_matching(job['description']))
            jobs_with_scores.append({
                'job': dict(job),
                'score': 0  # Will be updated with similarity score
            })
            
        # Calculate TF-IDF vectors
        try:
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
        except ValueError as e:
            print(f"Error in TF-IDF calculation: {e}")
            return []
        
        # Calculate cosine similarity between resume and all jobs
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
        # Update similarity scores
        for i, score in enumerate(cosine_similarities):
            jobs_with_scores[i]['score'] = score
        
        # Sort by similarity score (descending)
        jobs_with_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Extract just the job data for the top N matches
        job_matches = [item['job'] for item in jobs_with_scores[:top_n]]
        
        logger.debug(f"Calculated {len(cosine_similarities)} similarity scores")
        logger.debug(f"Returning {len(job_matches)} job matches")
        
        return job_matches
        
    def get_job_by_id(self, job_id):
        # Retrieve a specific job by ID
        db = get_db()
        job = db.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
        if job:
            return dict(job)
        return None