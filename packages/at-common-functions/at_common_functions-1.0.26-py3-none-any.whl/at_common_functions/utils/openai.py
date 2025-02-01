import logging
from openai import AsyncOpenAI
import httpx
from dataclasses import dataclass

@dataclass
class OpenAISettings:
    organization: str
    api_key: str
    proxy: str

class OpenAIService:
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init(self, settings: OpenAISettings):
        if not self._is_initialized:
            if settings.proxy == "":
                self._client = AsyncOpenAI(
                    api_key=settings.api_key,
                    organization=settings.organization
                )
            else:
                self._client = AsyncOpenAI(
                    api_key=settings.api_key,
                    organization=settings.organization,
                    http_client=httpx.AsyncClient(proxy=settings.proxy)
                )
            self._is_initialized = True

    async def chat(self, system: str, user: str, model: str, output_format: str = 'text', temperature: float = 0.0, max_tokens: int = 8192):
        if model in {'o1', 'o1-preview', 'o1-mini', 'o3', 'o3-mini'}:
            messages = [{"role": "user", "content": f"{system}\n\n{user}"}]
            max_token_key = "max_tokens"
        else:
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
            max_token_key = "max_completion_tokens"

        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            max_token_key: max_tokens
        }
        
        if output_format == 'json':
            params["response_format"] = {"type": "json_object"}
        
        response = await self._client.chat.completions.create(**params)
        return response.choices[0].message.content
        
# Global instance
_openai_service = OpenAIService()

def init_openai(settings: OpenAISettings) -> OpenAIService:
    _openai_service.init(settings)
    return _openai_service

def get_openai() -> OpenAIService:
    if not _openai_service._is_initialized:
        raise RuntimeError("OpenAI service not initialized. Call init_openai first.")
    return _openai_service