from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma



    client = chromadb.PersistentClient(path="/db")
    collection = client.create_collection(name="my_collection")
    collection.add(
        documents=["This is a document", "This is another document"],
        metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=["id1", "id2"]
    )












# class Vectorstore():
#     def __init__(self, path='./db'):
#         self.store = Chroma.PersistentClient(path)
#         self.files = []

#     def update_store(self, chunks, file_name):
#         # Create vector store from chunks
#         if file_name not in self.files:
#             self.store = Chroma.from_documents(chunks, OpenAIEmbeddings())
#             self.files.append(file_name)
#         else:
#             print('이미 벡터데이터가 존재합니다.')
#         return self.store

#     def clear_store(self):
#         self.store.reset()
        
