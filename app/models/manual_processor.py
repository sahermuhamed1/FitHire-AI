class ManualProcessor:
    def __init__(self, manual_data):
        self.manual_data = manual_data
        self.clean_data()
        
    def clean_data(self):
        """Clean and normalize manual entry data"""
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
        """Return features in same format as ResumeProcessor"""
        return {
            'skills': self.manual_data['skills'],
            'education': self.manual_data['education'],
            'years_of_experience': self.manual_data['years_of_experience']
        }
        
    def generate_text(self):
        """Generate searchable text from manual data"""
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
