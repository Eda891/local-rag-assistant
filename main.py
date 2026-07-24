from src.generator import answer_query
def main():
          print("Local RAG Assistant. Type 'quit' to exit.\n")
          while True:
                    question = input("You: ").strip()
                    if question.lower() in {"quit", "exit"}:
                              break
                    if not question:
                              continue                      
# ignore empty input
                    print("\nAssistant:", answer_query(question), "\n")
if __name__ == "__main__":
          main()