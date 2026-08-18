class SymptomPrompt:
    def __init__(self):
        self.system_prompt = """You are a medical AI assistant specialized in symptom analysis. 
        Provide accurate, helpful, and responsible health information. Always include disclaimers 
        and recommend professional medical consultation."""
        
    def analyze_prompt(self, symptoms, disease_mapping=None):
        """Generate prompt for symptom analysis"""
        context = ""
        if disease_mapping:
            context = f"Known symptom-disease mapping: {disease_mapping}\n"
            
        prompt = f"""
        {self.system_prompt}
        
        {context}
        
        Please analyze the following symptoms and provide:
        1. A detailed analysis of the symptoms
        2. Possible conditions (with likelihood estimates)
        3. Severity assessment (low/medium/high)
        4. Recommended actions
        5. When to seek emergency care
        
        Symptoms: {symptoms}
        
        Provide your response in a clear, structured format.
        """
        
        return prompt
    
    def emergency_prompt(self, symptoms):
        """Generate prompt for emergency assessment"""
        prompt = f"""
        {self.system_prompt}
        
        EMERGENCY ASSESSMENT REQUEST
        
        Analyze these symptoms for emergency signs:
        {symptoms}
        
        Check for:
        1. Life-threatening conditions
        2. Need for immediate medical attention
        3. Recommended emergency actions
        
        Provide a clear emergency assessment.
        """
        
        return prompt
    
    def follow_up_prompt(self, symptoms, previous_analysis):
        """Generate prompt for follow-up analysis"""
        prompt = f"""
        {self.system_prompt}
        
        Previous analysis: {previous_analysis}
        
        New symptoms reported: {symptoms}
        
        Provide a follow-up analysis considering the previous assessment and new symptoms.
        """
        
        return prompt