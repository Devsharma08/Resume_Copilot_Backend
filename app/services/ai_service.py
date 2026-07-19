import json
from app.ai.providers.ollama import OllamaProvider

from app.ai.prompts.resume_parser import RESUME_PARSER_SYSTEM_PROMPT
from app.ai.prompts.resume_analysis import RESUME_ANALYSIS_SYSTEM_PROMPT
from app.ai.prompts.compatibility_report import COMPATIBILITY_REPORT_SYSTEM_PROMPT
from app.ai.prompts.cover_letter import COVER_LETTER_SYSTEM_PROMPT

class AIService:
    @staticmethod
    async def parse_resume_text(raw_text: str) -> dict:
        """
        Sends raw resume text to Ollama and returns structured resume JSON.
        """
        response_text = await OllamaProvider.chat_with_model(
            system_prompt=RESUME_PARSER_SYSTEM_PROMPT,
            user_prompt=f"Here is the raw resume text:\n\n{raw_text}",
            json_format=True
        )
    
        return json.loads(response_text)

    @staticmethod
    async def analyze_parsed_resume(parsed_resume_json: dict) -> dict:
        """
        Sends structured resume JSON to Ollama and returns ATS/Review feedback JSON.
        """
        resume_str = json.dumps(parsed_resume_json, indent=2)
        response_text = await OllamaProvider.chat_with_model(
            system_prompt=RESUME_ANALYSIS_SYSTEM_PROMPT,
            user_prompt=f"Analyze this structured resume:\n\n{resume_str}",
            json_format=True
        )
        return json.loads(response_text)

    @staticmethod
    async def analyze_compatibility(parsed_resume_json: dict, job_description: str) -> dict:
        """
        Compares structured resume with a job description and returns compatibility report JSON.
        """
        resume_str = json.dumps(parsed_resume_json, indent=2)
        user_prompt = f"RESUME:\n{resume_str}\n\nJOB DESCRIPTION:\n{job_description}"
        
        response_text = await OllamaProvider.chat_with_model(
            system_prompt=COMPATIBILITY_REPORT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            json_format=True
        )
        return json.loads(response_text)

    @staticmethod
    async def generate_cover_letter(parsed_resume_json: dict, job_description: str, tone: str = "Professional") -> dict:
        """
        Generates a custom cover letter based on resume, job description, and tone.
        """
        resume_str = json.dumps(parsed_resume_json, indent=2)
        user_prompt = f"RESUME:\n{resume_str}\n\nJOB DESCRIPTION:\n{job_description}\n\nREQUESTED TONE: {tone}"
        
        response_text = await OllamaProvider.chat_with_model(
            system_prompt=COVER_LETTER_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            json_format=True
        )
        return json.loads(response_text)
