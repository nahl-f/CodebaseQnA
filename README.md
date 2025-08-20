# CodebaseQnA

**CodebaseQnA** lets you talk to your codebase in natural language. Instead of digging through files or searching manually, you can ask questions like *“Where is the `User` class defined?”* or *“How does the login function work?”* and get direct, context-aware answers from your own code.

It uses **retrieval-augmented generation (RAG)** powered by a local **Ollama LLM**, semantic embeddings, and a vector database to make your codebase conversational.

---

## 🚀 Features
- Query your codebase in **natural language**.
- Get explanations, references, and code snippets directly from your files.
- **CLI mode**: run in your terminal and chat without leaving your IDE.  
- **GUI mode**: use the Gradio interface with syntax highlighting for a smoother reading experience.
- Works locally with **Llama 3.2**, **nomic-embed-text**, **LangChain**, and **Chroma**.

---

## ⚙️ How It Works
1. Your codebase is embedded into a **vector database (ChromaDB)**.  
2. On each query, semantically relevant code snippets are retrieved.  
3. The snippets are added to the prompt and sent to a **local Ollama model**.  
4. The model generates an answer with explanations and references to the right files.  

---

## 🛠️ Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/nahl-f/CodebaseQnA.git
   cd CodebaseQnA
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on macOS/Linux
   venv\Scripts\activate      # on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Make sure you have [Ollama](https://ollama.ai/) installed and the required models (`llama3.2` and `nomic-embed-text`) available.

---

## 💻 Usage

### CLI (terminal chat)
```bash
python chat.py
```
You’ll be prompted to provide the path to your codebase, then you can start chatting with it directly from your terminal.

### GUI (Gradio interface)
```bash
python uichat.py
```
You’ll be prompted to provide the path to your codebase, then you can start chatting with it directly from your terminal. This will launch a *Gradio* browser interface with syntax highlighting.

