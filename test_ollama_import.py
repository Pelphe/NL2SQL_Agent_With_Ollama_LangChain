from langchain_community.llms.ollama import Ollama

llm = Ollama(model="llama3", temperature=0.0)
print("Ollama import and initialization successful!")
