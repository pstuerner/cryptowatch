import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.utils.custom import CustomOpenAIEmbeddings
from backend.utils.env import OPENAI_KEY

class ChromaDB:
    def __init__(self) -> None:
        self.client = self._connect()

    def _connect(self):
        client = chromadb.HttpClient(host='localhost', port=8000)
        openai_ef = CustomOpenAIEmbeddings(
                openai_api_key=OPENAI_KEY,
        )
        collection = client.get_or_create_collection(name="articles", embedding_function=openai_ef)

        return Chroma(
            client=client,
            collection_name="articles",
            embedding_function=openai_ef,
        )
    
    def insert(self, article):
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(article.pop("content"))
        self.client.add_documents(
            documents=[
                Document(
                    page_content=c,
                    metadata={
                        "title": article["title"],
                        "url": article["url"],
                        "published": article["published"]
                    }
                ) for c in chunks
            ],
            ids=[f"{article['url']}_{i}" for i, _ in enumerate(chunks)]
        )
    
    def query(self, q, k=5, filter={}):
        return self.client.similarity_search(
            q,
            k=k,
            filter=filter,
        )
