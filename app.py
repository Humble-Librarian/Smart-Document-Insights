import streamlit as st
from utils.parser import parse_pdf
from utils.retriever import build_index, retrieve_pages
from utils.generator import generate_answer

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Smart Document Insights", layout="wide")

# ── Session state initialization ─────────────────────────────────────────────
for key, default in {"pages": None, "bm25": None, "chat_history": []}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📄 Smart Document Insights")
    st.caption("AI-powered PDF Q&A — upload a document and ask questions.")

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        # Only re-parse when a new file is uploaded
        if st.session_state.get("_uploaded_name") != uploaded_file.name:
            with st.spinner("Parsing document…"):
                pages = parse_pdf(uploaded_file)

            if not pages:
                st.error(
                    "This PDF has no extractable text. "
                    "Please upload a text-based PDF."
                )
                st.session_state.pages = None
                st.session_state.bm25 = None
                st.session_state.chat_history = []
                st.session_state["_uploaded_name"] = None
            else:
                st.session_state.pages = pages
                st.session_state.bm25 = build_index(pages)
                st.session_state.chat_history = []
                st.session_state["_uploaded_name"] = uploaded_file.name

        # Show document info
        if st.session_state.pages:
            st.success(f"**{uploaded_file.name}** loaded")
            st.metric("Total pages", len(st.session_state.pages))
    else:
        st.info("👆 Upload a PDF to get started.")

# ── Main area ────────────────────────────────────────────────────────────────
st.title("Smart Document Insights")
st.markdown("Ask natural-language questions about any PDF document.")

# Render chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Re-render source expander for assistant messages that have sources
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander("📑 View Source Pages"):
                for src in msg["sources"]:
                    st.markdown(f"**Page {src['page']}**")
                    st.text(src["text"][:500])
                    st.divider()

# Chat input
query = st.chat_input("Ask a question about your document…")

if query:
    # Guard: no PDF uploaded
    if st.session_state.pages is None:
        st.warning("Please upload a PDF first.")
        st.stop()

    # Show user message
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Retrieve & generate
    retrieved = retrieve_pages(
        st.session_state.bm25, st.session_state.pages, query
    )

    with st.chat_message("assistant"):
        response = st.write_stream(generate_answer(retrieved, query))

        with st.expander("📑 View Source Pages"):
            for page in retrieved:
                st.markdown(f"**Page {page['page']}**")
                st.text(page["text"][:500])
                st.divider()

    # Save assistant message with sources for history re-rendering
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response, "sources": retrieved}
    )
