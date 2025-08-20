from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever, rootname
from terminal import printart
import gradio as gr
from rich import print as rprint
model = OllamaLLM(model = "llama3.2")

template = """
You are an expert software engineer and a helpful assistant for a codebase. Your goal is to answer questions about the provided code, its logic, and its structure. You must use the provided codebase context to answer the user's question. Do not invent information or mention files that are not present in the context.
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
        old_history = chat_history[:-max_convo*2] #stores everything except the last 15 interactions , the last indice is basically use counting from the end of the list backwards
        new_history = chat_history[-max_convo*2:] #stores only the last 15 interactions

        str_old = "\n".join(old_history)

        history_template = "Summarize this conversation history into a concise paragraphi that preserves important details, decisions, and context {str_old}"
        hprompt = ChatPromptTemplate.from_template(history_template)
        summarychain = hprompt | model
        summary = summarychain.invoke({"str_old" : str_old})

        rprint("[yellow]\nSummary: [/yellow]", summary)

        return [f"(Earlier summary) {summary}"] + new_history

def chathistory():
    rprint(f"\n [grey66]{chat_history}[/grey66]")
    return chat_history
printart(rootname)
def chat_response(message, history):
    chat_history = chathistory()
    chat_history = summarise_history(chat_history)
    chat_history.append(f"User: {message}")
    context = retriever.invoke(message)
    result = chain.invoke({"context" : context, "question" : message, "chat_history" : chat_history})
    chat_history.append(f"AI: {result}")

    return result

ui = gr.ChatInterface(fn = chat_response,
                      title="Codebase QNA",
                      textbox=gr.Textbox(placeholder="Ask me any question about your codebase!", container=False, scale=7),
                      theme = gr.themes.Ocean()
                      )

ui.launch()