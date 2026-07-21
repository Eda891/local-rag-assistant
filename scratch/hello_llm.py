from foundry_local_sdk import Configuration,FoundryLocalManager

MODEL_ALIAS="qwen2.5-0.5b"

#start the foundary local service for the app
config=Configuration(app_name="rag-assistant")
print("1. initializing...")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

#register the execution provider
manager.download_and_register_eps()

#fetch download and load the model into memory
print("3. getting model...")
model = manager.catalog.get_model(MODEL_ALIAS)
print("4. downloading...")
model.download()
print("5. loading...")
model.load()
print("6. done, chatting...")

#the SDK hands us its own chat client no OpenAI client needed
client=model.get_chat_client()
messages= [
          {"role": "system", "content": "You are a helpful, concise assistant."},
          {"role": "user", "content": "Explain what Dragons are in two sentences."},
]

# Stream the answer piece by piece as the model generates it
print("Asistant:",end="",flush=True)
for chunk in client.complete_streaming_chat(messages):
          if chunk.choices:
                  piece=chunk.choices[0].delta.content
                  if piece:
                          print(piece,end="",flush=True)
print()

model.unload() #free the memory when done