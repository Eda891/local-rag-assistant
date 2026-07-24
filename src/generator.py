from foundry_local_sdk import Configuration, FoundryLocalManager
from src.config import LLM_ALIAS
from src.retriever import get_top_chunks
_client = None
def _get_client():
    global _client
    if _client is None:
        print("[1/6] Creating Foundry configuration...")
        config = Configuration(app_name="rag_assistant")

        print("[2/6] Initializing FoundryLocalManager...")
        FoundryLocalManager.initialize(config)
        manager = FoundryLocalManager.instance

        print("[3/6] Downloading/registering execution providers...")
        manager.download_and_register_eps()

        print(f"[4/6] Fetching model catalog entry for '{LLM_ALIAS}'...")
        model = manager.catalog.get_model(LLM_ALIAS)

        print("[5/6] Downloading model (skips if already cached)...")
        model.download()

        print("[6/6] Loading model into memory...")
        model.load()

        print("Getting chat client...")
        _client = model.get_chat_client()   # loaded once, reused every call
        print("Client ready.")
    return _client


SYSTEM_PROMPT = (
    "You are a helpful assistant that answers ONLY using the provided context. "
    "If the answer is not in the context, say: \"I don't have that information.\" "
    "Cite the source document name in your answer."
)


def answer_query(question: str) -> str:
    print("Retrieving top chunks...")
    chunks = get_top_chunks(question)
    print(f"Got {len(chunks)} chunks.")

    client = _get_client()

    # 1. Build the context block from the retrieved chunks.
    context_parts = []
    for chunk in chunks:
        context_parts.append(f"[source: {chunk['source']}]\n{chunk['content']}")
    context = "\n\n".join(context_parts)

    # 2. Build the user message.
    user_message = f"{context}\n\nQuestion: {question}"

    # 3. Build the messages list.
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    # 4. Stream the reply and accumulate it into a string.
    print("Sending request to model, waiting for first token...")
    answer = ""
    first_token = True
    for chunk in client.complete_streaming_chat(messages):
        if chunk.choices:
            piece = chunk.choices[0].delta.content
            if piece:
                if first_token:
                    print("First token received! Streaming...")
                    first_token = False
                answer += piece

    print("Stream complete.")
    return answer

if __name__ == "__main__":
    print(answer_query("What should I do during an earthquake?"))