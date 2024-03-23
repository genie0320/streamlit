from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

def get_response(query, chat_history):

    template = """
    You are my friendly mental counselor. 
    I am a person with depression, and I am very lonely. 
    Answer my questions in a positive way by referring to chat_history. 
    If necessary, guide me through questions so that I can change my mind on my own.
    Answer in question's language.

    Chat history: {chat_history}

    User question: {query}
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    # output_parser = StrOutputParser(response)

    chain = prompt | llm | StrOutputParser()

    ai_responce = chain.stream({
        'chat_history' : chat_history,
        'query' : query,}
        )
    
    return ai_responce


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# st.set_page_config(page_title = 'Chat Bot', page_icon = '👀')
st.title("Chat Bot")

for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message('Human'):
            st.markdown(msg.content)

    else :
        with st.chat_message('AI'):
            st.markdown(msg.content)

# User input
query =st.chat_input("Enter your name")

# Conversation
if query is not None and query!= "":
    st.session_state.chat_history.append(HumanMessage(query))

    with st.chat_message('Human'):
        st.markdown(query)

    with st.chat_message('AI'):
        # st.markdown(AIMessage(query))
        ai_response = st.write_stream(get_response(query, st.session_state.chat_history))
        

    st.session_state.chat_history.append(AIMessage(ai_response))

