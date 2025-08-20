from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from chunkgeneration import generatedchunks
from rich import print as rprint
import os
import sys

cur_dir = str(input("\rEnter your codebases directory: "))

rootname = os.path.basename(cur_dir)
embeddings = OllamaEmbeddings(model = 'nomic-embed-text')

#creating the documents for embedding
def createdocuments(chunkdict):
    documents = []
    for filepath, chunks in chunkdict.items():
        for chunk in chunks:
            item_doc = Document(
                page_content=chunk,
                metadata={"source": filepath},
            )
            documents.append(item_doc)
    rprint("\n:heavy_check_mark: [bright_green]Codebase is being indexed......[/bright_green]")
    return documents

db_location = './chroma_db'

#creating the chroma database
vector_store = Chroma(
        collection_name = "codebase", 
        persist_directory = db_location,
        embedding_function = embeddings
)

chunkdict = generatedchunks(cur_dir)
if chunkdict:
    for filepath in chunkdict:
        vector_store._collection.delete(where={"source" : filepath})
    documents = createdocuments(chunkdict)
    rprint(":heavy_check_mark: [bright_green]Refreshed embeddings![/bright_green]")
    vector_store.add_documents(documents=documents)
    rprint("\n:heavy_check_mark: [purple]Database Updated [/purple]")

retriever = vector_store.as_retriever(
    search_kwargs = {"k":10}
)