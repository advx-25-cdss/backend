from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


def construct_prompt(transcription: str) -> str:
    return f"""You are a clinical expert who is summarizing the conversation between a patient and a doctor.
The patient is describing their symptoms and the doctor is asking questions to understand the patient's condition.
Please note that the transcription and summarization is continuous, so you should summarize the conversation as it progresses.
We could not tell patient and physician apart, so you should summarize the conversation as a whole.
Your output language should be the same as the input language.

Please provide a structured summary including:
1. Chief complaints or main symptoms mentioned
2. Key questions asked by the doctor
3. Patient responses and additional details
4. Any medical history mentioned
5. Assessment or next steps discussed

Here is the transcription of the conversation: {transcription}

Summary:"""


class TranscriptionSummarizer:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        try:
            # Use a lighter model that's more suitable for summarization
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            self.model_loaded = True
            print(f"Successfully loaded summarization model: {model_name}")
            
        except Exception as e:
            print(f"Failed to load model {model_name}: {e}")
            print("Falling back to rule-based summarization")
            self.model_loaded = False
            self.tokenizer = None
            self.model = None

    def generate_summary(self, transcription: str) -> str:
        """Generate a summary of the conversation"""
        try:
            if not self.model_loaded:
                return self._rule_based_summary(transcription)
            
            # Construct the prompt
            prompt = construct_prompt(transcription)
            
            # Tokenize the input
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=1024, truncation=True)
            
            # Generate summary
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 200,  # Allow for 200 new tokens
                    min_length=inputs.shape[1] + 50,   # Minimum 50 new tokens
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1,
                    no_repeat_ngram_size=3
                )
            
            # Decode the generated text
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the summary part (after "Summary:")
            if "Summary:" in generated_text:
                summary = generated_text.split("Summary:")[-1].strip()
            else:
                summary = generated_text[len(prompt):].strip()
                
            return summary if summary else self._rule_based_summary(transcription)
            
        except Exception as e:
            print(f"Error generating AI summary: {e}")
            return self._rule_based_summary(transcription)

    def _rule_based_summary(self, transcription: str) -> str:
        """Fallback rule-based summarization when AI model is not available"""
        lines = transcription.split('\n')
        
        # Extract key information
        symptoms = []
        questions = []
        responses = []
        
        for line in lines:
            line_lower = line.lower()
            
            # Look for symptom keywords
            symptom_keywords = ['pain', 'hurt', 'ache', 'fever', 'cough', 'headache', 'nausea', 'dizzy', 'tired', 'swelling']
            if any(keyword in line_lower for keyword in symptom_keywords):
                symptoms.append(line.strip())
            
            # Look for questions (contains question marks or question words)
            if '?' in line or any(qword in line_lower for qword in ['what', 'when', 'where', 'how', 'why', 'which']):
                questions.append(line.strip())
            else:
                responses.append(line.strip())
        
        # Build structured summary
        summary_parts = []
        
        if symptoms:
            summary_parts.append(f"Symptoms mentioned: {'; '.join(symptoms[:3])}")  # Top 3 symptoms
        
        if questions:
            summary_parts.append(f"Key questions: {'; '.join(questions[:2])}")  # Top 2 questions
            
        if responses:
            summary_parts.append(f"Patient responses: {'; '.join(responses[:2])}")  # Top 2 responses
        
        summary_parts.append(f"Total conversation length: {len(lines)} segments")
        
        return ' | '.join(summary_parts) if summary_parts else "No significant content detected in conversation."

    def extract_key_points(self, transcription: str) -> dict:
        """Extract key points from the conversation in a structured format"""
        summary = self.generate_summary(transcription)
        
        # Basic extraction of key information
        key_points = {
            "chief_complaints": [],
            "symptoms": [],
            "questions_asked": [],
            "medical_history": [],
            "assessment": [],
            "total_segments": len(transcription.split('\n')),
            "summary": summary
        }
        
        # Simple keyword extraction
        lines = transcription.lower().split('\n')
        
        for line in lines:
            # Chief complaints
            if any(word in line for word in ['complain', 'problem', 'issue', 'concern']):
                key_points["chief_complaints"].append(line.strip())
            
            # Symptoms
            if any(word in line for word in ['pain', 'hurt', 'fever', 'cough', 'headache', 'nausea']):
                key_points["symptoms"].append(line.strip())
            
            # Questions
            if '?' in line:
                key_points["questions_asked"].append(line.strip())
            
            # Medical history
            if any(word in line for word in ['history', 'previous', 'before', 'past', 'family']):
                key_points["medical_history"].append(line.strip())
            
            # Assessment/plan
            if any(word in line for word in ['diagnosis', 'treatment', 'medication', 'follow', 'next']):
                key_points["assessment"].append(line.strip())
        
        # Limit to top items to avoid overwhelming
        for key in key_points:
            if isinstance(key_points[key], list) and len(key_points[key]) > 3:
                key_points[key] = key_points[key][:3]
        
        return key_points


# Initialize global summarizer instance
summarizer_instance = None

def get_summarizer():
    """Get or create the global summarizer instance"""
    global summarizer_instance
    if summarizer_instance is None:
        summarizer_instance = TranscriptionSummarizer()
    return summarizer_instance
