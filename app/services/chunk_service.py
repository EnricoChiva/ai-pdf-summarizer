from typing import List
import re
import tiktoken


def chunk_text(text: str, max_tokens: int = 1000, model: str = "gpt-4") -> List[str]:
    """
    Zerlegt Text in semantische Absätze und splittet diese hart,
    wenn sie größer als max_tokens sind.
    """

    # Tokenizer laden, Fallback falls Modell unbekannt
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    def token_count(s: str) -> int:
        return len(encoding.encode(s))

    # Absätze erkennen
    sections = re.split(r'\n\s*\n', text)
    chunks: list[str] = []
    current_chunk = []
    current_tokens = 0

    for section in sections:
        section = section.strip()
        if not section:
            continue

        section_tokens = token_count(section)

        # Wenn Hinzufügen des Abschnitts den Chunk sprengt
        if current_tokens + section_tokens > max_tokens:
            if current_chunk:
                chunks.append(" ".join(current_chunk).strip())
            current_chunk = [section]
            current_tokens = section_tokens
        else:
            current_chunk.append(section)
            current_tokens += section_tokens

        # Falls ein Abschnitt zu groß ist → hart splitten
        while current_tokens > max_tokens:
            big_section = current_chunk.pop()
            tokens = encoding.encode(big_section)
            while len(tokens) > max_tokens:
                part = tokens[:max_tokens]
                chunks.append(encoding.decode(part))
                tokens = tokens[max_tokens:]
            if tokens:
                leftover = encoding.decode(tokens)
                current_chunk.append(leftover)
                current_tokens = token_count(" ".join(current_chunk))
            else:
                current_tokens = 0

    # Letzten Chunk anhängen
    if current_chunk:
        chunks.append(" ".join(current_chunk).strip())

    return chunks
