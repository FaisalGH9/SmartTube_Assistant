from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

chat_chains = {}

def get_smart_chain(video_id):
    if video_id in chat_chains:
        return chat_chains[video_id]

    embedding = OpenAIEmbeddings()
    vectordb = Chroma(
        persist_directory=f"./data/{video_id}/chroma",
        embedding_function=embedding
    )
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=1000,
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"  # ✅ Tells memory to track only the 'answer' field
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )

    chat_chains[video_id] = chain
    return chain
