import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekModel:
    def __init__(self, model_path: str = "deepseek-ai/deepseek-coder-7b-base"):
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        self.tokenizer = None
        self.model = None
        
    def load_model(self):
        """Load the DeepSeek model and tokenizer."""
        try:
            logger.info("Loading DeepSeek tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            
            logger.info("Loading DeepSeek model...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
                device_map="auto",
                trust_remote_code=True
            )
            
            logger.info("Model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def generate_summary(self, title: str, abstract: str) -> Optional[Dict[str, str]]:
        """Generate a structured summary using DeepSeek."""
        if not self.model or not self.tokenizer:
            if not self.load_model():
                return None
        
        try:
            prompt = f"""Please analyze the following scientific paper and create a structured summary with these sections:
Title: {title}

Abstract: {abstract}

Please provide:
1. Objective: The main goal or purpose of the study
2. Methods: Key methodological approaches used
3. Results: Main findings and outcomes
4. Conclusions: Primary conclusions and implications
5. Limitations: Study limitations or constraints

Format each section clearly and indicate if any section cannot be determined from the provided information."""

            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=1000,
                    temperature=0.3,
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Parse the response into sections
            sections = self._parse_response(response)
            return sections
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return None
    
    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse the model response into structured sections."""
        sections = {
            'objective': 'Not available in abstract',
            'methods': 'Not available in abstract',
            'results': 'Not available in abstract',
            'conclusions': 'Not available in abstract',
            'limitations': 'Not available in abstract'
        }
        
        try:
            # Split response into lines and process each line
            current_section = None
            current_text = []
            
            for line in response.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                lower_line = line.lower()
                
                # Check for section headers
                if 'objective:' in lower_line:
                    current_section = 'objective'
                    current_text = [line.split(':', 1)[1].strip()]
                elif 'methods:' in lower_line:
                    if current_section and current_text:
                        sections[current_section] = ' '.join(current_text)
                    current_section = 'methods'
                    current_text = [line.split(':', 1)[1].strip()]
                elif 'results:' in lower_line:
                    if current_section and current_text:
                        sections[current_section] = ' '.join(current_text)
                    current_section = 'results'
                    current_text = [line.split(':', 1)[1].strip()]
                elif 'conclusions:' in lower_line:
                    if current_section and current_text:
                        sections[current_section] = ' '.join(current_text)
                    current_section = 'conclusions'
                    current_text = [line.split(':', 1)[1].strip()]
                elif 'limitations:' in lower_line:
                    if current_section and current_text:
                        sections[current_section] = ' '.join(current_text)
                    current_section = 'limitations'
                    current_text = [line.split(':', 1)[1].strip()]
                elif current_section:
                    current_text.append(line)
            
            # Add the last section
            if current_section and current_text:
                sections[current_section] = ' '.join(current_text)
            
        except Exception as e:
            logger.error(f"Error parsing response: {str(e)}")
        
        return sections

# Initialize global model instance
model = DeepSeekModel() 