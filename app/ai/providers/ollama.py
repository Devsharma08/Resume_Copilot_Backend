import httpx
import json
from typing import Any

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME="qwen2.5:1.5b"

class OllamaProvider:
    @staticmethod
    async def chat_with_model(
        system_prompt:str,
        user_prompt:str,
        json_format:bool = False
    )->str:
       """
        Sends a system instruction and user prompt to local Ollama.
        
        Parameters:
        - system_prompt: Instructions outlining how the AI should behave (e.g. RESUME_PARSER_SYSTEM_PROMPT).
        - user_prompt: The actual content (e.g. the resume raw text).
        - json_format: If True, forces Ollama to output valid JSON.
        """
        message = [
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ]

        payload = {
            "model":MODEL_NAME,
            "messages":message,
            "options":{"temperature": 0.3},
            "stream":False
        } 
        
        if json_format:
            payload["format"] = "json"

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(OLLAMA_URL,json=payload)
                response.raise_for_status() # raises HTTPError for bad responses (4xx or 5xx)
                
                # --- NEW: STRICT JSON FIX ---
                result = response.json()

                # Ollama returns the result in message["content"]
                return result["message"]["content"]
            except Exception as e:
                raise RuntimeError(f"failed to communicate with local ollama service: {str(e)}")
