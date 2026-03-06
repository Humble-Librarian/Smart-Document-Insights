import streamlit as st
from utils.parser import parse_pdf
from utils.retriever import build_index, retrieve_pages
from utils.generator import generate_answer

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Document Insights",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Stylish expanders for sources */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: #88C0D0 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #4C566A;
        border-radius: 8px;
        margin-top: 10px;
    }
    /* Metric styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #88C0D0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ── Session state initialization ─────────────────────────────────────────────
for key, default in {"pages": None, "bm25": None, "chat_history": []}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.shields.io/badge/Smart%20Document-Insights-6366F1?style=for-the-badge&logo=googledrive&logoColor=white", use_container_width=True)
    st.markdown("---")
    
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Drop your PDF here", type=["pdf"], label_visibility="collapsed")

    if uploaded_file is not None:
        # Only re-parse when a new file is uploaded
        if st.session_state.get("_uploaded_name") != uploaded_file.name:
            with st.spinner("Analyzing document structure…"):
                pages = parse_pdf(uploaded_file)

            if not pages:
                st.error("⚠️ This PDF has no extractable text. Please upload a standard text PDF.")
                st.session_state.pages = None
                st.session_state.bm25 = None
                st.session_state.chat_history = []
                st.session_state["_uploaded_name"] = None
            else:
                st.session_state.pages = pages
                with st.spinner("Building AI retrieval index…"):
                    st.session_state.bm25 = build_index(pages)
                st.session_state.chat_history = []
                st.session_state["_uploaded_name"] = uploaded_file.name

        # Show document info cleanly
        if st.session_state.pages:
            st.success("✅ Document Ready", icon="🟢")
            st.metric("Total Pages Indexed", len(st.session_state.pages))
    else:
        st.info("👆 Upload a PDF to activate the intelligence engine.")
        
    st.markdown("---")
    with st.expander("ℹ️ How it works"):
        st.markdown(
            """
            1. **Upload**: Drop any text-based PDF.
            2. **Index**: The app instantly parses and indexes all pages.
            3. **Ask**: Ask natural language questions.
            4. **Discover**: Advanced AI retrieves the exact pages and streams context-aware answers.
            """
        )

# ── Main area ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 15])
with col1:
    st.markdown("<h1 style='text-align: center; margin-top: -10px;'>📄</h1>", unsafe_allow_html=True)
with col2:
    st.title("Smart Document Insights")
st.markdown("#### *Uncover the truth in your documents with real-time AI analysis.*")
st.markdown("---")

# Render chat history
for msg in st.session_state.chat_history:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander("📑 View Source Evidence"):
                for src in msg["sources"]:
                    st.markdown(f"**Page {src['page']}**")
                    st.caption(src["text"][:600] + "...")
                    st.divider()

# Chat input
query = st.chat_input("Ask a question about the uploaded document…")

if query:
    if st.session_state.pages is None:
        st.warning("⚠️ Please upload and index a PDF first.")
        st.stop()

    # Show user message
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(query)

    # Retrieve & generate
    with st.spinner("Searching document context..."):
        retrieved = retrieve_pages(st.session_state.bm25, st.session_state.pages, query)

    with st.chat_message("assistant", avatar="🤖"):
        response = st.write_stream(generate_answer(retrieved, query))

        with st.expander("📑 View Source Evidence"):
            for page in retrieved:
                st.markdown(f"**Page {page['page']}**")
                st.caption(page["text"][:600] + "...")
                st.divider()

    st.session_state.chat_history.append(
        {"role": "assistant", "content": response, "sources": retrieved}
    )
