import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

def process_and_store(video_id, transcript_json):
    # Combine segments with timestamps
    segments = transcript_json["segments"]
    full_text = ""
    for seg in segments:
        content = seg["text"].strip()
        start = seg["start"]
        timestamp = f"[{int(start // 60)}:{int(start % 60):02d}]"
        full_text += f"{timestamp} {content}\n"

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.create_documents([full_text])

    # Store chunks as vector embeddings
    embedding = OpenAIEmbeddings()
    db_path = f"./data/{video_id}/chroma"
    db = Chroma.from_documents(docs, embedding, persist_directory=db_path)
    db.persist()

def load_chain(video_id):
    embedding = OpenAIEmbeddings()
    db_path = f"./data/{video_id}/chroma"
    db = Chroma(persist_directory=db_path, embedding_function=embedding)

    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
