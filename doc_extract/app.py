"""AI Document Extractor — Streamlit UI"""

import streamlit as st
import pandas as pd
from parser import parse_pdf
from extractor import extract
from schemas import InvoiceData

st.set_page_config(page_title="📑 AI Document Extractor", layout="wide")
st.title("📑 AI Document Extractor")
st.caption("Upload invoice or resume PDFs — AI extracts structured data into clean tables")

files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

if files and st.button("🚀 Extract All"):
    results = []
    for f in files:
        with st.spinner(f"Processing {f.name}..."):
            text = parse_pdf(f.read())
            doc_type, data = extract(text)
            results.append({"filename": f.name, "type": doc_type, "data": data})

    # Group by type
    invoices = [r for r in results if r["type"] == "invoice"]
    resumes = [r for r in results if r["type"] == "resume"]

    if invoices:
        st.subheader(f"🧾 Invoices ({len(invoices)})")
        rows = []
        for r in invoices:
            d = r["data"]
            rows.append({"File": r["filename"], "Invoice No": d.invoice_no, "Vendor": d.vendor,
                         "Date": d.date, "Total": d.total, "Tax": d.tax, "Grand Total": d.grand_total})
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Download CSV", df.to_csv(index=False), "invoices.csv", "text/csv")

        # Show line items per invoice
        for r in invoices:
            with st.expander(f"Line items — {r['filename']}"):
                st.dataframe(pd.DataFrame([item.model_dump() for item in r["data"].items]))

    if resumes:
        st.subheader(f"📄 Resumes ({len(resumes)})")
        rows = []
        for r in resumes:
            d = r["data"]
            rows.append({"File": r["filename"], "Name": d.name, "Email": d.email,
                         "Phone": d.phone, "Skills": ", ".join(d.skills)})
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Download CSV", df.to_csv(index=False), "resumes.csv", "text/csv")

        # Show experience per resume
        for r in resumes:
            with st.expander(f"Details — {r['filename']}"):
                st.write("**Experience**")
                st.dataframe(pd.DataFrame([e.model_dump() for e in r["data"].experience]))
                st.write("**Education**")
                st.dataframe(pd.DataFrame([e.model_dump() for e in r["data"].education]))
