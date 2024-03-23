from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter

import chromadb  
import streamlit as st

load_dotenv()

def get_chunked(url):
    headers_to_split_on = [
        ("h1", "Header 1"),
        ("h2", "Header 2"),
        ("h3", "Header 3"),
        ("h4", "Header 4"),
    ]
    html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    # for local file use html_splitter.split_text_from_file(<path_to_file>)
    html_header_splits = html_splitter.split_text_from_url(url)

    chunk_size = 500
    chunk_overlap = 30
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    # Split - 근데 이렇게 자르면 메타데이터가 붙지 않는다.
    splits = text_splitter.split_documents(html_header_splits)

    return splits


def get_response(query, chat_history, vector_store):

    template = """
    Answer the user's questions by referring to the given data and in the context of 'chat history'
    Say you don't know about the parts you don't know.
    If you need anything to answer correctly, ask the user a question.

    reference data : {reference_article}
    Chat history: {chat_history}
    User question: {user_query}
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    # output_parser = StrOutputParser(response)
    retriever = vector_store.as_retriever()
    reference_article = retriever.get_relevant_documents(query)
    
    # chain = prompt | llm | StrOutputParser()

    # ai_response = chain.stream({
    #     'chat_history' : chat_history,
    #     'user_query' : query,
    #     'reference_article' : reference_article,
    #     }
    # )
    return reference_article

# Page Template
st.title("3_Chat_with_Web")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# sidebar
with st.sidebar:
    st.header('Settings')
    website_url = st.text_input('Website URL')

if website_url == "":
    st.info('Please enter your website url')
else:
    # Chroma
    client = chromadb.PersistentClient(path="/db")
    collection = client.create_collection(name="my_collection")
    collection.add(
        documents=["This is a document", "This is another document"],
        metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=["id1", "id2"]
    )
    results = collection.query(
        query_texts=["document"],
        n_results=2
    )
    results
    db = get_store(website_url)
    
    with st.sidebar:
        st.write(db)
        
    with st.chat_message('AI'):
        st.markdown(f'{website_url} 에 대한 대화를 시작합니다.')

    for msg in st.session_state.chat_history:
        if isinstance(msg, HumanMessage):
            with st.chat_message('Human'):
                st.markdown(msg.content)
        else :
            with st.chat_message('AI'):
                st.markdown(msg.content)

    query =st.chat_input("Enter your name")

    # Conversation
    if query is not None and query!= "":
        st.session_state.chat_history.append(HumanMessage(query))
        with st.chat_message('Human'):
            st.markdown(query)
        with st.chat_message('AI'):
            ai_response = st.write_stream(get_response(query, st.session_state.chat_history, db))
            st.session_state.chat_history.append(AIMessage(ai_response))



# Chroma db를 어떻게 활용했었는지 기억이 안난다. 자꾸만 embedding 해서 같은 데이터가 백만개 나오는 상태.
# 그리고 chunking이 매우 이상하게 되어 있음. 그냥 평범하게 바꿔야겠다.
# https://python.langchain.com/docs/modules/data_connection/retrievers/vectorstore

# Building a Generative AI app with Streamlit and OpenAI
# https://freedium.cfd/https://levelup.gitconnected.com/building-a-generative-ai-app-with-streamlit-and-openai-95ec31fe8efd

# Working With Files in Python
# https://realpython.com/working-with-files-in-python/