import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.path["PDF_PATH"] = os.getenv("PDF_PATH")


loader = PyPDFLoader(os.path["PDF_PATH"])  # ← Put your healthcare PDF here
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
splits = text_splitter.split_documents(documents)

# Chroma + Gemini (handles 3072 dims automatically )
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db"  # Local storage
)

print(f"SUCCESS! Stored {len(splits)} chunks in ./chroma_db")
