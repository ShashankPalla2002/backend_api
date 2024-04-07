import os
from dotenv import load_dotenv
import google.generativeai as genai

class LLM:
    def __init__(self, logger):
        load_dotenv()
        self.logger  = logger
        self.api_key = os.getenv("GEMINI_KEY")
        self.model   = os.getenv("GEMINI_MODEL")

    
    def generate_response(self, value):
        try:
            if self.api_key == None:
                self.logger.error(f"api_key is None")

            if self.model == None:
                self.logger.error(f"model is None")

            genai.configure(api_key=self.api_key)
            load_model = genai.GenerativeModel(self.model)
            self.logger.info(f"loaded model successfuly")

            prompt = f'''
            **Input:** Keyword
            **Task:** Explain the keyword in about 50 words, focusing on its technical aspects.
            **Guidelines:**
            1. Start the definition with the provided keyword.
            2. Avoid mentioning any specific organizations (e.g., Google, Microsoft).
            3. If the keyword isn't related to technology, software, or programming, provide "None" as output.
            4. If the keyword is a person's name, provide "None" as output.
            5. Also give a technical level skill that one should acquire to learn the keyword. Only give the skills individually. Ex: data structures, data analysis, data engineering, programming languages, devops, etc.

            **Keyword:** {value}
            '''
            self.logger.info(f"prompt: {prompt}")

            response = load_model.generate_content(prompt)
            self.logger.info(f"generated response: {response}")

            return response.text
        
        except Exception as e:
            self.logger.error(f"error while generating response: {e}")