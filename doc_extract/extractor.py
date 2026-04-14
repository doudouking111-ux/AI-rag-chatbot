"""LLM structured extraction using Pydantic + with_structured_output."""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME
from schemas import InvoiceData, ResumeData

llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    temperature=0,
)

CLASSIFY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Classify the document as 'invoice' or 'resume'. Return only one word."),
    ("human", "{text}"),
])

EXTRACT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Extract structured information from the following document. Be precise and thorough."),
    ("human", "{text}"),
])


def classify_doc(text: str) -> str:
    """Classify document type: 'invoice' or 'resume'."""
    resp = (CLASSIFY_PROMPT | llm).invoke({"text": text[:500]})
    return "invoice" if "invoice" in resp.content.lower() else "resume"


def extract(text: str, doc_type: str | None = None) -> tuple[str, BaseModel]:
    """Extract structured data. Returns (doc_type, pydantic_object)."""
    if doc_type is None:
        doc_type = classify_doc(text)

    schema = InvoiceData if doc_type == "invoice" else ResumeData
    chain = EXTRACT_PROMPT | llm.with_structured_output(schema)
    result = chain.invoke({"text": text})
    return doc_type, result
