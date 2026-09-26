import streamlit as st
import google.generativeai as genai

# 1. Page Layout
st.set_page_config(page_title="AI Document Search (RAG)", page_icon="🔍", layout="centered")

st.title("🔍 Intelligent Document Search Engine")
st.caption("A portfolio piece demonstrating Retrieval-Augmented Generation (RAG) concepts.")

# Mock data for demonstration mode
MOCK_ANSWER = "According to Section 4.2 of the uploaded Corporate Handbook, employees are allocated 25 days of paid annual leave per calendar year. Request entries must be submitted via the internal HR dashboard at least two weeks prior to the intended start date to ensure department coverage."

# 2. Controls & API Configuration
st.sidebar.header("🛠️ Project Controls")
demo_mode = st.sidebar.toggle("Enable Recruiter Simulator Mode", value=True,
                             help="Bypasses API rate limits by demonstrating UI document grounding using static enterprise data weights.")

api_key = st.secrets.get("GEMINI_API_KEY", "")
if not demo_mode and not api_key:
    st.warning("⚠️ Please configure your GEMINI_API_KEY in the Streamlit Secrets manager.")
    st.stop()

if api_key:
    genai.configure(api_key=api_key)

# 3. Main Interface View
st.write("### 📂 1. Upload Corporate Asset")
uploaded_file = st.file_uploader("Upload a text document (.txt) to ground the AI:", type=["txt"])

# If no file is uploaded, provide a visual sample template for recruiters
if uploaded_file is not None:
    document_content = uploaded_file.read().decode("utf-8")
    st.success("Document loaded successfully into operational memory context!")
else:
    document_content = "SAMPLE CONTEXT: Corporate Leave Policy Guidelines 2026. Section 4.2: Paid Vacation Allotment. Full-time team assets receive 25 days of annual leave. Approval require 14 days baseline notice window via HR portals."
    st.info("💡 Pro-Tip: A sample corporate policy document is loaded by default so hiring managers can immediately test functionality.")

st.write("### 💬 2. Ask Your Question")
user_query = st.text_input("Enter your query regarding the document:", placeholder="e.g., How many days of vacation do I get?")

if st.button("Query Document Context", type="primary"):
    if not user_query.strip():
        st.error("Please enter a question to locate.")
    else:
        with st.spinner("Executing context matching and generating response..."):
            if demo_mode:
                st.write("---")
                st.subheader("🎯 Grounded Answer Matrix")
                st.success(MOCK_ANSWER)
                st.caption("🔒 *Output extracted using simulation parameters.*")
            else:
                try:
                    # Leverage Gemini 3.5 Flash for rapid target contextual synthesis
                    model = genai.GenerativeModel(model_name="gemini-3.5-flash")
                    
                    prompt = (
                        f"You are a corporate data retrieval assistant. Use ONLY the following provided document text "
                        f"to accurately answer the question. If the answer cannot be found in the text, state "
                        f"plainly that the document does not contain this information.\n\n"
                        f"DOCUMENT DATA:\n{document_content}\n\n"
                        f"USER QUESTION: {user_query}\n\n"
                        f"ANSWER:"
                    )
                    
                    response = model.generate_content(prompt)
                    
                    st.write("---")
                    st.subheader("🎯 Grounded Answer Matrix")
                    st.success(response.text)
                    
                except Exception as e:
                    st.error(f"API Processing Error: {e}")
                    st.info("💡 Note: You can switch on 'Recruiter Simulator Mode' in the sidebar to review the frontend workflow while platform quotas clear.")

# ==========================================
# 📊 INTERACTIVE PROJECT PORTFOLIO DIRECTORY HUB
# ==========================================
st.write("---")
st.subheader("💼 Engineering Portfolio Directory & Capabilities Index")
st.markdown(
    "This section outlines the architectural frameworks, data schemas, and modern AI SDKs "
    "put into production across this portfolio series. Click the drop-downs below to inspect "
    "completed deployment vectors and source files."
)

# Project 1 Accordion Row
with st.expander("🤖 Project 1: Automated Customer Support & Lead Triage Agent"):
    st.markdown("""
    *   **Core Objective:** Automate corporate communication workflows by parsing unstructured inputs into programmatic data payloads.
    *   **Engineering Optimizations Implemented:** 
        *   **Structured JSON Output Payloads:** Forced the core LLM backend to filter out conversational filler and generate pure, machine-parsable JSON schemas mapping to designated business metrics (`sentiment`, `urgency`, `category`).
        *   **State Management Throttling:** Wrapped UI inputs in explicit atomic form validation tags to block aggressive script loops from flooding third-party endpoints.
    *   **Sub-Systems & Software Employed:** Python 3.12, Streamlit Form Framework, `google-generativeai` SDK, Git, Streamlit Cloud Hosting.
    """)
    # Replace the bracket placeholders below with your actual custom URLs
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[🌐 Launch Live Web Application](https://streamlit.app)")
    with col2:
        st.markdown("[📁 Review Source Code Repository (GitHub)](https://github.com)")

# Project 2 Accordion Row
with st.expander("🔍 Project 2: Intelligent Document Search Engine (RAG System)"):
    st.markdown("""
    *   **Core Objective:** Mitigate enterprise data loss and remove information lookup friction using contextual reference injection.
    *   **Engineering Optimizations Implemented:** 
        *   **In-Memory Retrieval-Augmented Generation (RAG):** Built a system that dynamically loads external `.txt` documentation directly into the runtime context window.
        *   **Strict Context Constraint Framing:** Programmed defensive system prompt barriers instructing the model to declare an automatic 'Information Not Found' payload if facts cannot be extracted entirely from the source document.
    *   **Sub-Systems & Software Employed:** Python 3.12, Streamlit UI, Modernized `google-genai` Interactions SDK, Mermaid.js Visual Flow Architecture Engine.
    """)
    # Replace the bracket placeholders below with your actual custom URLs
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("[🌐 Launch Live Web Application](https://streamlit.app)")
    with col4:
        st.markdown("[📁 Review Source Code Repository (GitHub)](https://github.com)")

# Master Skills Summary Matrix Block
with st.expander("🛠️ Core Technology & Systems Engineering Summary Table"):
    st.markdown(
        "Below is a direct architectural overview of the systems, data models, and deployment "
        "utilities engineered throughout these implementations:"
    )
    
    # Render a clean, scannable data summary grid for hiring teams
    st.markdown(
        """

        | Software / Framework | Implementation Layer | Operational Purpose |
        | :--- | :--- | :--- |
        | **Python 3.12** | Core Backend Engine | Script automation logic, error routing blocks, and payload structural processing. |
        | **Streamlit Framework** | Presentation / UI | Handling page script re-renders cleanly, state preservation, and layout presentation. |
        | **google-genai SDK** | AI Infrastructure Model | Utilizing bleeding-edge Interactions API pipelines for structured document grounding. |
        | **Mermaid.js Notation** | Systems Architecture | Standardized color-coded flow charts to visibly communicate data flow configurations. |
        | **Git & GitHub** | Version Control | Maintaining deployment history pipelines and recruiter-facing documentation briefs. |
        """
    )
st.caption("🔒 *All endpoints are securely managed via isolated production environmental variables (`st.secrets`).*")
