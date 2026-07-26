from foundry_local_sdk import Configuration,FoundryLocalManager

MODEL_ALIAS="qwen2.5-0.5b"

config=Configuration(app_name="rag-assistant")
print("1. initializing...")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

manager.download_and_register_eps()

print("3. getting model...")
model = manager.catalog.get_model(MODEL_ALIAS)
print("4. downloading...")
model.download()
print("5. loading...")
model.load()
print("6. done, chatting...")

client=model.get_chat_client()
messages= [
          {"role": "system", "content": "You are a helpful, concise assistant."},
          {"role": "user", "content": "Explain what Dragons are in two sentences."},
]

print("Asistant:",end="",flush=True)
for chunk in client.complete_streaming_chat(messages):
          if chunk.choices:
                  piece=chunk.choices[0].delta.content
                  if piece:
                          print(piece,end="",flush=True)
print()

model.unload() 