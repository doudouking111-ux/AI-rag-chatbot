"""AI Invoice Processor — Streamlit UI"""

import streamlit as st
import pandas as pd
from pipeline import run_pipeline
from storage import load_all

st.set_page_config(page_title="🧾 AI Invoice Processor", layout="wide")
st.title("🧾 AI Invoice Processor")
st.caption("Upload invoice PDF → AI extracts info → Save to spreadsheet → Send notification")

uploaded = st.file_uploader("Upload Invoice PDF", type=["pdf"])

if uploaded and st.button("🚀 Process"):
    with st.spinner("Processing..."):
        result = run_pipeline(uploaded.read(), uploaded.name)

    st.subheader("① Raw Text")
    st.text_area("Extracted from PDF", result["raw_text"], height=150)

    st.subheader("② AI Extraction Result")
    st.json(result["extracted"])

    if result["extracted"].get("items"):
        st.dataframe(pd.DataFrame(result["extracted"]["items"]))

    st.subheader("③ Storage")
    st.success(f"Saved to `{result['csv_path']}`")

    st.subheader("④ Notification")
    st.info(result["notification"])

# Show history
records = load_all()
if records:
    st.divider()
    st.subheader("📋 Processing History")
    st.dataframe(pd.DataFrame(records))
