from src.config import CHUNK_MAX_CHARS

def chunk_text(text: str) -> list[str]:
    """Split text into chunks of roughly CHUNK_MAX_CHARS characters."""
    paragraphs = text.split("\n\n")

    chunks = []
    current = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if current and len(current) + len(para) > CHUNK_MAX_CHARS:
            chunks.append(current.strip())
            current = para
        else:
            if current:
                current += "\n\n" + para
            else:
                current = para

    if current.strip():
        chunks.append(current.strip())

    return chunks