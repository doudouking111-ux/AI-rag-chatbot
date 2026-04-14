"""AI structured extraction: extract key fields from invoice text."""

import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    temperature=0,
)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an invoice extraction assistant. Extract the following fields from the invoice text and return JSON:
- invoice_no: invoice number
- vendor: vendor/supplier name
- date: date (YYYY-MM-DD)
- items: list of line items, each with name, quantity, unit_price, amount
- total: subtotal amount
- tax: tax amount (if any)
- grand_total: total including tax

Return only JSON, no other text."""),
    ("human", "{text}"),
])

chain = PROMPT | llm


def extract_invoice(text: str) -> dict:
    """Extract structured data from invoice text using LLM."""
    resp = chain.invoke({"text": text})
    return json.loads(resp.content)
