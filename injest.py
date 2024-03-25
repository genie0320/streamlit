#%%
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter # langchain-text-splitters
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
# from transformers import AutoTokenizer

import os

def load_html(data_folder = 'data/for_loader/'):
    docs = []

    files = os.listdir(data_folder)

    for file in files[3:]:
        file = data_folder + file
        loader = UnstructuredHTMLLoader(file)
        data = loader.load()
        docs.extend(data)
        
    return docs

def get_chunks(docs, chunk_len=300):
    MARKDOWN_SEPARATORS = [
        "\n#{1,6} ",
        "```\n",
        "\n\\*\\*\\*+\n",
        "\n---+\n",
        "\n___+\n",
        "\n\n",
        "\n",
        " ",
        "",
    ]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_len,  # the maximum number of characters in a chunk: we selected this value arbitrarily
        chunk_overlap=chunk_len*0.1,  # the number of characters to overlap between chunks
        # add_start_index=True,  # If `True`, includes chunk's start index in metadata
        strip_whitespace=True,  # If `True`, strips whitespace from the start and end of every document
        separators=MARKDOWN_SEPARATORS,
    )

    chunks = text_splitter.split_documents(docs)

    return chunks

def set_db(chunks) -> None:
    EMBEDDING_MODEL_NAME = 'jhgan/ko-sbert-nli'
    # embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    ko_embed = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    Chroma.from_documents(chunks, embedding=ko_embed, persist_directory=".chroma/" )

def get_db() -> Chroma:
    EMBEDDING_MODEL_NAME = 'jhgan/ko-sbert-nli'
    # embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    ko_embed = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    db = Chroma(persist_directory=".chroma/", embedding_function=ko_embed)
    
    return db

def clear_db(db):
    db.delete()
    print('삭제가 완료되었습니다.')

#%%
docs = load_html()

#%%
chunks = get_chunks(docs)
#%%
set_db(chunks)

#%%
db = get_db()
retriever = db.as_retriever(search_type="mmr")
query="시간을 잘 사용하는 방법"
res = retriever.get_relevant_documents(query)
print(res)

#%%
# DB삭제
ids = db.get()['ids']
print(len(ids))
# db.delete(ids)


# %%
