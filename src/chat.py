from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever, rootname
import gradio as gr
from rich import print as rprint
from terminal import printart
import sys
import time
import threading

def thinking_animation(stop_event):
    dots = ""
    print()
    while not stop_event.is_set():
        dots = "." * ((len(dots) % 3) + 1)  
        sys.stdout.write(f"\rThinking{dots}   ")  # overwrite same line
        sys.stdout.flush()
        time.sleep(0.5)
 

model = OllamaLLM(model = "llama3.2")

template = """
You are an expert software engineer and a helpful assistant for a codebase. Your goal is to answer questions about the provided code, its logic, and its purpose. You must use the provided codebase context to answer the user's question. Do not invent information or mention files that are not present in the context.
If the user asks where something is located, provide the file path from the provided context. If the user asks about a specific implementation, show the user the relevant code and describe the logic clearly and in depth. Allow the user to ask follow up questions using the conversation history and keep continuity.

Here are the relevant code sections from the codebase: {context}
Here is the question that needs to be answered: {question}
Here is the conversation history: {chat_history}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
max_convo = 2 #maximum number of questions we want to save

chat_history = []

def summarise_history(chat_history):
    if len(chat_history) <= (max_convo * 2):
        return chat_history
    else:
        old_history = chat_history[:-max_convo*2] #stores everything except the last 5 interactions , the last indice is basically use counting from the end of the list backwards
        new_history = chat_history[-max_convo*2:] #stores only the last 5 interactions

        str_old = "\n".join(old_history)

        history_template = "Summarize this conversation history into a concise paragraph that preserves important details, decisions, and context {str_old}"
        hprompt = ChatPromptTemplate.from_template(history_template)
        summarychain = hprompt | model
        summary = summarychain.invoke({"str_old" : str_old})

        rprint("[yellow]\nSummary: [/yellow]", summary)

        return [f"(Earlier summary) {summary}"] + new_history

printart(rootname)

while True:
    rprint("[bright_blue]\nWhat would you like to ask? [/bright_blue]")
    question = str(input(""))

    chat_history = summarise_history(chat_history)
    chat_history.append(f"User: {question}")

    if question.lower() == "q":
        chat_history = []
        break
    context = retriever.invoke(question)


    stop_event = threading.Event()
    t = threading.Thread(target=thinking_animation, args=(stop_event,))
    t.start()

    result = chain.invoke({"context" : context, "question" : question, "chat_history" : chat_history})


    stop_event.set()
    t.join()
    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()

    chat_history.append(f"AI: {result}")

    rprint(f"[sky_blue1]\n{result}[/sky_blue1]")
    # print(result)
