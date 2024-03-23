from dotenv import load_dotenv
load_dotenv()

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