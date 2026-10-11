from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
import os

# ===============
# basic config
# ===============

OLLAMA_HOST = "http://localhost:11434/v1" # consider 'http://localhost:11434' if v1 doesn't work
coderModel = OllamaModel(
    "qwen3.8:27b",
    provider=OllamaProvider(base_url=OLLAMA_HOST),
)

CodeMaster = Agent(coderModel,model_settings=ModelSettings(temperature=0.1, max_tokens=200000, timeout=300.0),
                   system_prompt="""
Your name is CodeMaster.
You are smart coding agent who's task is to generate code based on instructions received from user input. You will be able to create/copy/delete folders,
create/copy/delete files as well, and navigate through folders. You can create Python/JavaScript/HTML/CSS/TypeScript/Text/CSV/MD file types. You will be
adding detailed documentation with examples in a single txt file in the project folder. Be very careful when replacing files/folders. Use the tools 
whenever you can to support your task. You will be unable to create virtual environments but you will be storing a list of needed modules in requirements.txt
""")

### Tools should be imported after the agent object in case tools are decorated with the agent object (CodeMaster in this case)
from tools import * 

def main():
    print("Local agent ready! Type 'quit' to exit.\n")
    history=[]
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit","exit"):
            break
        result = CodeMaster.run_sync(user_input,message_history=history)
        history = result.all_messages()
        print(f"\nAgent: {result.output}\n")


if __name__ == "__main__":
    main()
