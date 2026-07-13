import os

from django.conf import settings

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate


# -----------------------------
# Configuration
# -----------------------------

UPLOAD_DIR = settings.UPLOAD_DIR
DB_DIR = settings.CHROMA_DB_DIR


llm = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0,
)


def get_embedding_model():
    """
    Load the embedding model only when needed.
    This avoids loading torch during Django startup.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# -----------------------------
# Upload & Index PDF
# -----------------------------
def process_pdf(pdf_path):
    """
    Load PDF, split into chunks,
    create embeddings and save them in Chroma.
    """

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)

    embedding_model = get_embedding_model()

    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=DB_DIR,
    )

    return len(chunks)


# -----------------------------
# Ask Question
# -----------------------------
def ask_question(question):
    """
    Search relevant chunks and ask Groq.
    """

    if not os.path.exists(DB_DIR):
        return "Please upload a PDF first."

    embedding_model = get_embedding_model()

    vectordb = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embedding_model,
    )

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are an AI assistant.

Answer ONLY from the provided context.

If the answer is not found in the context, say:

"I couldn't find the answer in the uploaded document."

Context:
{context}

Question:
{question}
"""
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return response.content