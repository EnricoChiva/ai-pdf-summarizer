import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from app.config import settings


client = ChatCompletionsClient(
    endpoint=settings.azure_openai_endpoint,
    credential=AzureKeyCredential(settings.azure_openai_api_key)
)

userMessageContent_fulltext = """

"""

def summarize_text(text: str, max_tokens: int = 20000) -> str:
    """
    Nimmt langen Text und gibt eine Analyse/Struktur der PDF zurück.
    """
    response = client.complete(
        messages=[
            SystemMessage(content="""
You are an expert document analyst and knowledge extractor.
Your goal is to fully analyze long PDF documents.
Focus on understanding the entire content and extracting all important ideas.
Organize the extracted information into meaningful chapters or sections.
Ensure that the output is clear, professional, and factual.
"""),
            UserMessage(content=f"""
Analyze the following document thoroughly. 
1. Identify all key ideas and concepts.
2. Organize them into meaningful chapters/sections.
3. Under each chapter, list all important insights clearly and concisely.
4. Maintain the original language of the document.
5. Avoid unnecessary repetition. 
6. Provide the output in a structured and readable format (headings, bullet points if necessary).

Document content:
{text}
""")
        ],
        max_tokens=max_tokens,
        temperature=0.3,
        top_p=0.9,
        model=settings.azure_deployment_name
    )
    return response.choices[0].message.content.strip()
