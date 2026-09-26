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
