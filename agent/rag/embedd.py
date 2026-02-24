# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from qdrant_client import QdrantClient
# from qdrant_client.http.models import Distance, VectorParams
# from langchain_qdrant import QdrantVectorStore  # New class name

# load_dotenv()
# os.environ["GOOGLE_API_KEY"] = "AIzaSyAY1umlKh3FNyLpQyWRExU995MlPsO2IuY"

# # Load and split
# loader = PyPDFLoader("az_bank.pdf")
# documents = loader.load()
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(documents)

# embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# # ✅ FIXED: Check if exists + correct 3072 dims
# client = QdrantClient(path="./qdrant_db")
# if not client.collection_exists("healthcare_docs"):
#     client.create_collection(
#         collection_name="healthcare_docs",
#         vectors_config=VectorParams(size=3072, distance=Distance.COSINE)  # FIXED dims!
#     )

# # ✅ New class name (no deprecation)
# vectorstore = QdrantVectorStore(
#     client=client, 
#     collection_name="healthcare_docs",
#     embeddings=embeddings
# )

# vectorstore.add_documents(splits)
# print("✅ Data ingested to local Qdrant DB!")

######################################################
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Load API key
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Load + split your PDF
loader = PyPDFLoader("az_bank.pdf")  # ← Put your healthcare PDF here
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
splits = text_splitter.split_documents(documents)

# Chroma + Gemini (handles 3072 dims automatically ✅)
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db"  # Local storage
)

print(f"✅ SUCCESS! Stored {len(splits)} chunks in ./chroma_db")
