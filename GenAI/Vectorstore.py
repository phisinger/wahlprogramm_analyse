from langchain.embeddings import GPT4AllEmbeddings
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
import chromadb


class Vectorstore_client:
    def __init__(self):
        self.persist_directory = "/home/phisinger/Programmieren/wahlprogramm_analyse/data/vectorstore"
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        elections = ["2013", "2017", "2021"]
        for election in elections:
            # load all files from cleaned data set
            glob = "*" + election + ".txt"
            loader = DirectoryLoader(
                '/home/phisinger/Programmieren/wahlprogramm_analyse/data/clean/', glob=glob, use_multithreading=True, loader_cls=TextLoader)
            docs_list = loader.load()
            # split documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200)
            all_splits = text_splitter.split_documents(docs_list)
            all_texts = [text.page_content for text in all_splits]
            # generate ids for all documents
            ids_list = ["id{}".format(i)
                        for i in range(1, len(all_texts) + 1)]
            # Store splits in database
            collection = self.client.get_or_create_collection(
                name=election)
            if collection.count() == 0:
                collection.add(
                    documents=all_texts,
                    ids=ids_list
                )
        return

    def get_client(self):
        return self.client


# class Vectorstore:
#     def __init__(self) -> None:
#         self.persist_directory = "/home/phisinger/Programmieren/wahlprogramm_analyse/data/vectorstore"
#         if False:
#             # load data from data persist_directory
#             print("use persisted db.")
#             self.vectordb = Chroma(persist_directory=persist_directory,
#                                    embedding_function=GPT4AllEmbeddings())
#         else:
#             print("Build new vector DB")
#             self.build_vectorstore()

#         return self.vectordb

#     def build_vectorstore(self):
#         elections = ["2013", "2017", "2021"]
#         for election in elections:
#             # load all files from cleaned data set
#             glob = "*" + election + ".txt"
#             loader = DirectoryLoader(
#                 '../data/clean/', glob=glob, use_multithreading=True, loader_cls=TextLoader)
#             docs_list = loader.load()
#             # split documents
#             text_splitter = RecursiveCharacterTextSplitter(
#                 chunk_size=1000, chunk_overlap=200)
#             all_splits = text_splitter.split_documents(docs_list)
#             # store documents in vector store
#             self.vectordb = Chroma.from_documents(
#                 documents=all_splits, embedding=GPT4AllEmbeddings(), persist_directory=self.persist_directory)
#             self.vectordb.persist()

#         def get(self):
#             return self.vectordb
