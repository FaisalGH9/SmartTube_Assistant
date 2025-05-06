from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

agent_map = {}

def get_agent_executor(video_id):
    if video_id in agent_map:
        return agent_map[video_id]

    embedding = OpenAIEmbeddings()
    vectordb = Chroma(
        persist_directory=f"./data/{video_id}/chroma",
        embedding_function=embedding
    )
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    def retrieval_tool_func(query):
        docs = retriever.get_relevant_documents(query)
        return "\n\n".join([doc.page_content for doc in docs])

    tools = [
        Tool(
            name="VideoTranscriptQA",
            func=retrieval_tool_func,
            description="Use this tool to answer questions using only the video transcript."
        )
    ]

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=1000,
        memory_key="chat_history",
        return_messages=True

    )

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True
    )

    agent_map[video_id] = agent
    return agent
