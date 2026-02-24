from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


def get_top_matches(query: str, k: int = 3) -> list:
    """
    Get top-K matches from ChromaDB for given query
    
    Args:
        query: Search query string
        k: Number of top results (default: 3)
    
    Returns:
        List of tuples: [(Document, score), ...] - lowest score = best match
    """
    # Load ChromaDB
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = Chroma(persist_directory="./rag/chroma_db", embedding_function=embeddings)
    
    # Get raw top-K results + scores
    results = vectorstore.similarity_search_with_score(query, k=k)
    
    return results