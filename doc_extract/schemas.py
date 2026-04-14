"""Pydantic schemas for structured extraction."""

from pydantic import BaseModel, Field


class LineItem(BaseModel):
    name: str
    quantity: str
    unit_price: str
    amount: str


class InvoiceData(BaseModel):
    invoice_no: str = Field(description="Invoice number")
    vendor: str = Field(description="Vendor/supplier name")
    date: str = Field(description="Invoice date (YYYY-MM-DD)")
    items: list[LineItem] = Field(description="Line items")
    total: float = Field(description="Subtotal before tax")
    tax: float = Field(description="Tax amount")
    grand_total: float = Field(description="Total including tax")


class Experience(BaseModel):
    company: str
    title: str
    period: str


class Education(BaseModel):
    school: str
    degree: str
    period: str


class ResumeData(BaseModel):
    name: str = Field(description="Full name")
    email: str = Field(default="", description="Email address")
    phone: str = Field(default="", description="Phone number")
    skills: list[str] = Field(description="Technical and professional skills")
    experience: list[Experience] = Field(description="Work experience")
    education: list[Education] = Field(description="Education background")
