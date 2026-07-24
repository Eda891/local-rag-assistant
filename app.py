# app.py
"""Field Terminal — offline knowledge assistant, forest-and-parchment theme."""
import streamlit as st
from src.generator import answer_query

st.set_page_config(page_title="Field Terminal", page_icon="🌲", layout="centered")

# --- Forest & parchment styling -------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Spectral:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp {
        background: radial-gradient(ellipse at top, #f4f6ef 0%, #eef1e6 55%, #e6ead9 100%);
        color: #2e2a20;
        font-family: 'JetBrains Mono', monospace;
    }

    .block-container {
        padding-top: 2.5rem;
        max-width: 700px;
    }

    /* Header band */
    .fh-header {
        border: 1px solid #6b5940;
        border-radius: 6px;
        padding: 22px 26px;
        margin-bottom: 20px;
        background: linear-gradient(135deg, rgba(143,174,122,0.12), rgba(196,154,91,0.07));
        position: relative;
    }
    .fh-eyebrow {
        font-size: 0.72rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #8a6a35;
        margin-bottom: 6px;
    }
    .fh-title {
        font-family: 'Spectral', serif;
        font-weight: 600;
        font-size: 2.1rem;
        color: #2e2a20;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .fh-sub {
        color: #5c5744;
        font-size: 0.85rem;
        margin-top: 8px;
    }
    .fh-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #5f7a52;
        margin-right: 8px;
        box-shadow: 0 0 6px #8fae7a;
    }

    /* Topic chips */
    .topics-label {
        font-size: 0.72rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #5c5744;
        margin-bottom: 10px;
    }
    .topic-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 26px;
    }
    .topic-chip {
        font-size: 0.78rem;
        padding: 6px 13px;
        border-radius: 20px;
        border: 1px solid;
        white-space: nowrap;
    }
    .chip-green {
        color: #3f5c33;
        border-color: #5f7a52;
        background: rgba(143,174,122,0.14);
    }
    .chip-brown {
        color: #6b4f28;
        border-color: #8a6a35;
        background: rgba(196,154,91,0.14);
    }
    .chip-beige {
        color: #5c5439;
        border-color: #8c7d5e;
        background: rgba(140,125,94,0.10);
    }

    h3 { color: #2e2a20 !important; font-family: 'Spectral', serif; }
    label, .stCaption, p { color: #5c5744 !important; }

    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #2e2a20;
        border: 1px solid #c3b89a;
        border-radius: 5px;
        font-family: 'JetBrains Mono', monospace;
        padding: 12px 14px;
    }
    .stTextInput > div > div > input:focus {
        border: 1px solid #5f7a52;
        box-shadow: 0 0 0 3px rgba(95, 122, 82, 0.15);
    }
    .stTextInput label {
        color: #8a6a35 !important;
        font-size: 0.78rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .stButton > button {
        background-color: #5f7a52;
        color: #f4f6ef;
        border: 1px solid #4a5c42;
        border-radius: 5px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
        letter-spacing: 1px;
        padding: 10px 24px;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #4a5c42;
        color: #f4f6ef;
        border: 1px solid #2e3a28;
    }

    .response-label {
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #5f7a52;
        margin-top: 26px;
        margin-bottom: 8px;
    }
    .response-box {
        background: #ffffff;
        border-left: 3px solid #c49a5b;
        border-radius: 4px;
        padding: 18px 22px;
        color: #2e2a20;
        line-height: 1.7;
        font-size: 0.95rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- Header ------------------------------------------------------------
st.markdown("""
<div class="fh-header">
    <div class="fh-eyebrow">Offline knowledge system</div>
    <p class="fh-title">🌲 Field Terminal</p>
    <div class="fh-sub"><span class="fh-dot"></span>foundry local · no internet required</div>
</div>
""", unsafe_allow_html=True)

# --- Topics you can ask about --------------------------------------------
st.markdown('<div class="topics-label">You can ask about</div>', unsafe_allow_html=True)
st.markdown("""
<div class="topic-row">
    <span class="topic-chip chip-green">🌪 natural disasters</span>
    <span class="topic-chip chip-brown">🏚 rebuilding civilization</span>
    <span class="topic-chip chip-beige">🏕 wilderness survival</span>
</div>
""", unsafe_allow_html=True)

# --- Query ---------------------------------------------------------------
question = st.text_input("QUERY", placeholder="ask your documents...")

if st.button("TRANSMIT") and question:
    with st.spinner("retrieving + generating..."):
        answer = answer_query(question)
    st.markdown('<div class="response-label">Response</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="response-box">{answer}</div>', unsafe_allow_html=True)