import chromadb
import uuid


from langchain.vectorstores import Chroma

from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

DATA_PATH = '../raw'
DB_FAISS_PATH = 'vectorstore/db_faiss'


# Create vector database
def create_vector_db():

    loader = DirectoryLoader('../raw', glob='./*.pdf', loader_cls=PyPDFLoader)

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    client = chromadb.HttpClient(host='localhost', port=8000)

    # the default embeddings are MiniLM-L6-v2, which is the same for Llama2
    collection = client.create_collection("accio_test")

    for doc in texts:
        collection.add(
            ids=[str(uuid.uuid1())], metadatas=doc.metadata, documents=doc.page_content
        )

    db = Chroma(client=client,
                collection_name="accio_test",
                embedding_function=embedding_function)

    query = "what is this legal agreement about"
    docs = db.similarity_search(query)
    print(docs[0].page_content)


if __name__ == "__main__":
    create_vector_db()



