import json
import re
from typing import Dict, Any
from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.GROQ_API_KEY, base_url=Config.GROQ_BASE_URL)

class InformationExtractor:
   """
    Extracts structured information from chat conversations using JSON schema.
    """
    
    def __init__(self):
        self.extraction_schema = {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Full name of the person"
                },
                "email": {
                    "type": "string",
                    "description": "Email address"
                },
                "phone": {
                    "type": "string",
                    "description": "Phone number in any format"
                },
                "location": {
                    "type": "string",
                    "description": "Location, address, city, or geographic information"
                },
                "age": {
                    "type": "integer",
                    "description": "Age in years"
                }
            },
            "required": []
        }
        
        self.function_definition = {
            "name": "extract_user_information",
            "description": "Extract user information from chat conversation",
            "parameters": self.extraction_schema
        }
    
    def extract_information(self, chat_text: str) -> Dict[str, Any]:
        """
        Extract structured information from chat using function calling
        """
        try:
            response = client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert at extracting personal information from chat conversations. 
                        Extract any mentioned name, email, phone, location, and age from the provided chat. 
                        Only extract information that is explicitly mentioned. Use null for missing information."""
                    },
                    {
                        "role": "user",
                        "content": f"Extract information from this chat:\n{chat_text}"
                    }
                ],
                functions=[self.function_definition],
                function_call={"name": "extract_user_information"},
                temperature=0.1
            )
            
            # Parse the function call response
            function_call = response.choices[0].message.function_call
            extracted_data = json.loads(function_call.arguments)
            
            # Clean up the data (remove null values and empty strings)
            cleaned_data = {k: v for k, v in extracted_data.items() 
                          if v is not None and v != ""}
            
            return cleaned_data
            
        except Exception as e:
            print(f"❌ Information extraction failed: {str(e)}")
            return {}
    
    def validate_extraction(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate extracted data against schema and provide quality metrics
        """
        validation_result = {
            "is_valid": True,
            "extracted_fields": list(extracted_data.keys()),
            "field_count": len(extracted_data),
            "validation_errors": []
        }
        
        # Check data types and formats
        for field, value in extracted_data.items():
            if field == "email" and value:
                if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
                    validation_result["validation_errors"].append(f"Invalid email format: {value}")
                    validation_result["is_valid"] = False
            
            elif field == "age" and value:
                if not isinstance(value, int) or value < 0 or value > 150:
                    validation_result["validation_errors"].append(f"Invalid age: {value}")
                    validation_result["is_valid"] = False
            
            elif field == "phone" and value:
                # Basic phone validation (digits and common separators)
                if not re.match(r'^[\d\s\-\+\(\)]{7,}$', str(value)):
                    validation_result["validation_errors"].append(f"Invalid phone format: {value}")
        
        return validation_result
