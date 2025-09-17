from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from app.config import settings
from openai import AzureOpenAI
from typing import List, Optional, Any
import logging
import asyncio

logger = logging.getLogger(__name__)


class AIService:
    """
    Wrapper around the AI clients (Maverick + O3).
    """
    
    def __init__(self, maverick_client: Optional[Any] = None, o3_client: Optional[Any] = None):
        self._maverick = (
            maverick_client
            if maverick_client is not None
            else ChatCompletionsClient(
                endpoint=settings.azure_openai_endpoint_maverick,
                credential=AzureKeyCredential(settings.azure_openai_api_key)
            )
        )

        self._o3 = (
            o3_client
            if o3_client is not None
            else AzureOpenAI(
                api_version=settings.api_version_o3,
                azure_endpoint=settings.azure_openai_endpoint_o3,
                api_key=settings.azure_openai_api_key
            )
        )

    async def _run_blocking(self,func, *args, **kwargs):
        """
        Führt eine blockierende Funktion in einem Thread aus, damit der Event-Loop frei bleibt.
        """
        return await asyncio.to_thread(lambda: func(*args, **kwargs))
    


    async def pre_summarize_chunks(self, text: str, max_tokens: int = 1000) -> str:
        """
        Analysiert einen Text-Chunk und liefert eine strukturierte, kurze Analyse/Zusammenfassung.
        Verwendet den 'Maverick' ChatCompletionsClient.
        """
        try:
            sys_msg = SystemMessage(
                content=(
                    "You are a concise and accurate document analyst. "
                    "Always produce verifiable, factual summaries. "
                    "When summarizing, keep to the limits requested and include a 'source' field "
                    "that references the chunk_id or page_number provided in the user message. "
                    "Avoid adding new claims not present in the text. If unsure, say 'uncertain' and mark it."
                )
            )
            user_msg = UserMessage(
                content=(
                    "Analyze the following document thoroughly.\n"
                    "1. Identify all key ideas and concepts.\n"
                    "2. Organize them into meaningful chapters/sections.\n"
                    "3. Under each chapter, list all important insights clearly and concisely.\n"
                    "4. Maintain the original language of the document.\n"
                    "5. Avoid unnecessary repetition.\n"
                    "6. Provide the output in a structured and readable format (headings, bullet points if necessary).\n\n"
                    f"Document content:\n{text}"
                )
            )

            def call_complete():
                return self._maverick.complete(
                    messages=[sys_msg, user_msg],
                    max_tokens=max_tokens,
                    temperature=0.3,
                    top_p=0.9,
                    model=settings.azure_deployment_name_maverick,
                )
            response = await self._run_blocking(call_complete)


            try:
                return response.choices[0].message.content.strip()
            except Exception:
                    text_out = getattr(response, "text", None) or getattr(response, "content", None)
                    if text_out:
                        return str(text_out).strip()
                    raise
        
        except Exception as exc:
             logger.exception("pre_summarize_chunks failed")
             raise




    async def summarize_text_o3_mini(self, text: str, max_tokens: int = 10000) -> str:
        """
        Kombiniert mehrere Chunk-Summaries (oder großen Text) zu einer finalen Zusammenfassung
        unter Verwendung des O3-Modells (oder wie in settings konfiguriert).
        """
        try:
            messages = [
                {"role": "system", "content": "You are an expert document analyst and knowledge extractor. Focus on factual, well-structured summaries."},
                {"role": "user", "content": f"Analyze the following document thoroughly and produce a clear, structured summary:\n\n{text}"},
            ]

            def call_o3():
                return self._o3.chat.completions.create(
                    messages=messages,
                    max_completion_tokens=max_tokens,
                    model=settings.azure_openai_model_o3
                )
            response = await self._run_blocking(call_o3)

            try:
                return response.choices[0].message.content.strip()
            except Exception:
                text_out = getattr(response, "text", None) or getattr(response, "content", None)
                if text_out:
                    return str(text_out).strip()
                raise
                
        except Exception:
            logger.exception("summarize_text_o3_mini failed")
            raise




    async def combine_summaries(self, single_simmaries: list[str]) -> str:
        """Kombiniert Chunk-Zusammenfassungen zu einer Gesamtübersicht."""
        if not single_simmaries:
            return ""
        
        all_summaries = "\n\n".join(single_simmaries)
        return await self.summarize_text_o3_mini(all_summaries)


    async def pre_summarize_many(self, texts: List[str], concurrency: int = 4) -> List[str]:
        """
        Helper: pre-summarize many texts with a concurrency limit to avoid rate limits.
        """
        sem = asyncio.Semaphore(concurrency)

        async def worker(t):
            async with sem:
                return await self.pre_summarize_chunks(t)

        return await asyncio.gather(*(worker(t) for t in texts))


_ai_service_singleton: Optional[AIService] = None


def get_ai_service() -> AIService:
    global _ai_service_singleton
    if _ai_service_singleton is None:
        _ai_service_singleton = AIService()
    return _ai_service_singleton