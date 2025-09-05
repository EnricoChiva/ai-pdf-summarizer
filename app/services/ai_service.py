from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from app.config import settings
from openai import AzureOpenAI

# Maverick-Client
client = ChatCompletionsClient(
    endpoint=settings.azure_openai_endpoint_maverick,
    credential=AzureKeyCredential(settings.azure_openai_api_key)
)

#OpenAI-Client
azure_client = AzureOpenAI(
     api_version=settings.api_version_o3,
     azure_endpoint=settings.azure_openai_endpoint_o3,
     api_key=settings.azure_openai_api_key
)

async def pre_summarize_chunks(text: str, max_tokens: int = 1000) -> str:
    """
    Nimmt Text und gibt eine Analyse/Struktur der PDF zurück.
    """
    response = client.complete(
        messages=[
            SystemMessage(content="""
You are a concise and accurate document analyst. 
Always produce verifiable, factual summaries. 
When summarizing, keep to the limits requested and include a 'source' field that references the chunk_id or page_number provided in the user message.
Avoid adding new claims not present in the text. If unsure, say "uncertain" and mark it.

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
        model=settings.azure_deployment_name_maverick
    )
    return response.choices[0].message.content.strip()


async def summarize_text_o3_mini(text: str, max_tokens: int = 10000) -> str:
    """
    Nimmt Text und gibt eine Analyse/Struktur der PDF zurück.
    """
    response = azure_client.chat.completions.create(
        messages=[
            {
                "role":"system",
                "content": """
You are an expert document analyst and knowledge extractor.
Your goal is to fully analyze long PDF documents.
Focus on understanding the entire content and extracting all important ideas.
Organize the extracted information into meaningful chapters or sections.
Ensure that the output is clear, professional, and factual.
"""
            },
            {
                "role": "user",
                "content": f"""
Analyze the following document thoroughly. 
1. Identify all key ideas and concepts.
2. Organize them into meaningful chapters/sections.
3. Under each chapter, list all important insights clearly and concisely.
4. Maintain the original language of the document.
5. Avoid unnecessary repetition. 
6. Provide the output in a structured and readable format (headings, bullet points if necessary).

Document content:
{text}
"""
            }
        ],
        max_completion_tokens=max_tokens,
        model=settings.azure_openai_model_o3
    )
    return response.choices[0].message.content.strip()



async def combine_summaries(single_simmaries: list[str]) -> str:
     """Kombiniert Chunk-Zusammenfassungen zu einer Gesamtübersicht."""
     all_summaries = "\n".join(single_simmaries)

     response = await summarize_text_o3_mini(all_summaries)
     return response