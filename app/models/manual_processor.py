class ManualProcessor:
    def __init__(self, manual_data):
        self.manual_data = manual_data
        self.clean_data()
        
    def clean_data(self):
        # Clean and normalize manual entry data
        # Clean skills
        self.manual_data['skills'] = [
            skill.strip().lower() 
            for skill in self.manual_data['skills'] 
            if skill.strip()
        ]
        
        # Clean education
        self.manual_data['education'] = [
            edu.strip() 
            for edu in self.manual_data['education'] 
            if edu.strip()
        ]
        
        # Ensure numeric experience
        try:
            self.manual_data['years_of_experience'] = int(self.manual_data['years_of_experience'])
        except:
            self.manual_data['years_of_experience'] = 0
            
    def extract_features(self):
        # Return features in same format as ResumeProcessor
        return {
            'skills': self.manual_data['skills'],
            'education': self.manual_data['education'],
            'years_of_experience': self.manual_data['years_of_experience']
        }
        
    def generate_text(self):
        # Generate searchable text from manual data
        sections = []
        
        # Add job title and industry
        if self.manual_data.get('job_title'):
            sections.append(f"Current Role: {self.manual_data['job_title']}")
        if self.manual_data.get('industry'):
            sections.append(f"Industry: {self.manual_data['industry']}")
            
        # Add summary
        if self.manual_data.get('summary'):
            sections.append(f"Professional Summary: {self.manual_data['summary']}")
            
        # Add skills
        if self.manual_data['skills']:
            sections.append("Skills: " + ", ".join(self.manual_data['skills']))
            
        # Add education
        if self.manual_data['education']:
            sections.append("Education: " + "; ".join(self.manual_data['education']))
            
        # Add experience
        if self.manual_data['years_of_experience']:
            sections.append(f"Years of Experience: {self.manual_data['years_of_experience']}")
            
        return "\n\n".join(sections)
        
    def evaluate_resume(self):
        """Evaluate resume quality as poor, good, very good, or excellent"""
        # Calculate a basic score based on manually entered features
        score = 0
        
        # Score based on skills
        skill_count = len(self.manual_data['skills'])
        if skill_count >= 10:
            score += 3  # Excellent skills section
        elif skill_count >= 6:
            score += 2  # Very good skills section
        elif skill_count >= 3:
            score += 1  # Good skills section
        # else Poor skills section (0 points)
        
        # Score based on education
        if self.manual_data['education']:
            advanced_degrees = ['master', 'ph', 'phd', 'doctor', 'mba']
            has_advanced = any(any(adv in str(edu).lower() for adv in advanced_degrees) for edu in self.manual_data['education'])
            if has_advanced:
                score += 2  # Advanced degree
            else:
                score += 1  # Has education listed
        
        # Score based on experience
        years = self.manual_data['years_of_experience']
        if years >= 5:
            score += 3  # Significant experience
        elif years >= 3:
            score += 2  # Good experience
        elif years >= 1:
            score += 1  # Some experience
        
        # Score based on summary quality (using length as a proxy)
        summary_length = len(self.manual_data.get('summary', ''))
        if summary_length >= 300:
            score += 2  # Detailed summary
        elif summary_length >= 150:
            score += 1  # Adequate summary
        
        # Map score to rating
        if score >= 8:
            return "excellent"
        elif score >= 6:
            return "very good"
        elif score >= 3:
            return "good"
        else:
            return "poor"
