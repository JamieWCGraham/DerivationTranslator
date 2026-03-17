"""Streamlit app for the Derivation Translator."""

from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from llm import explain_derivation
from parse import extract_text_from_pdf
from utils import truncate_preview

st.set_page_config(page_title="Derivation Translator", layout="centered")
st.title("Derivation Translator")
st.markdown(
    "A lightweight applied AI prototype that explains mathematical derivation steps. Upload a paper PDF or paste text, select a derivation excerpt, and get a structured explanation (steps, assumptions, intuition, ambiguities, confidence)."
)
st.divider()

# Source text: from PDF or manual paste
source_text = ""
pdf_upload = st.file_uploader("Upload PDF", type=["pdf"])
if pdf_upload:
    try:
        source_text = extract_text_from_pdf(pdf_upload)
        st.success("PDF text extracted.")
    except ValueError as e:
        st.error(str(e))
        source_text = ""

st.caption("Or paste text manually (overrides PDF if both are provided).")
manual_text = st.text_area(
    "Paste full text",
    height=120,
    placeholder="Paste paper or section text here…",
    label_visibility="collapsed",
)
if manual_text and manual_text.strip():
    source_text = manual_text.strip()
    if pdf_upload:
        st.info("Using manually pasted text (PDF text ignored).")

if source_text:
    preview = truncate_preview(source_text)
    with st.expander("Extracted / pasted text preview", expanded=False):
        st.text(preview)

st.divider()

derivation_input = st.text_area(
    "Derivation excerpt",
    height=150,
    placeholder="Paste the specific derivation lines you want explained…",
    help="Paste the exact derivation excerpt from the paper.",
)
context_input = st.text_area(
    "Optional context",
    height=80,
    placeholder="Optional: surrounding sentences or paragraph for disambiguation…",
    help="Additional context can improve accuracy.",
)

explain_clicked = st.button("Explain Derivation", type="primary")

if explain_clicked:
    if not derivation_input or not derivation_input.strip():
        st.error("Please paste a derivation excerpt to explain.")
    else:
        with st.spinner("Explaining…"):
            try:
                result = explain_derivation(
                    derivation_text=derivation_input.strip(),
                    context_text=context_input.strip() or None,
                )
            except ValueError as e:
                st.error(str(e))
                result = None

        if result:
            st.divider()
            st.subheader("Summary")
            st.write(result.summary)

            st.subheader("Step-by-step explanation")
            for step in result.steps:
                rule = f" — *{step.rule_or_operation}*" if step.rule_or_operation else ""
                st.markdown(f"**{step.step_number}.** {step.explanation}{rule}")

            st.subheader("Assumptions")
            if result.assumptions:
                for a in result.assumptions:
                    st.markdown(f"- {a}")
            else:
                st.caption("None listed.")

            st.subheader("Intuition")
            st.write(result.intuition)

            st.subheader("Ambiguities")
            if result.ambiguities:
                for a in result.ambiguities:
                    st.markdown(f"- {a}")
            else:
                st.caption("None listed.")

            confidence_label = result.confidence.replace("_", " ").capitalize()
            st.subheader("Confidence")
            st.caption(confidence_label)
