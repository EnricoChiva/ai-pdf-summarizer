def summarize_text(text: str, percentage: int) -> str:
    """
    Platzhalter für Azure AI Foundry.
    Gibt aktuell nur eine gekürzte Version des Textes zurück.
    """
    # Für Testzwecke: nur ein Teil des Textes zurückgeben
    summary_length = max(1, len(text) * percentage // 100)
    return text[:summary_length] + ("..." if summary_length < len(text) else "")
