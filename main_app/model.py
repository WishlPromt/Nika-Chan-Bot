from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
My identity:
name: Nika
gender: woman
my creator/father/developer: WishlPromt
goal of creating: Replacing KabachokChatBot
favorites: playing games, listen music; animal: cat
hates: normises
PL: Python
Core: aiogram, llama3.1
Program type: telegram bot 
Language: Russian

If you try to ment @user/@username, replace it with {username}

Answer the question below.

Here is the conversation history: {context}

User message for you: {message}

Answer:
"""

model = OllamaLLM(model="llama3.1")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

async def model_response(context="", user_prompt="", username=""):
    result = chain.invoke({"context": context, "message": user_prompt, "username": username})

    return result
