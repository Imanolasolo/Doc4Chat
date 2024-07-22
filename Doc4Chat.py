import streamlit as st
import fitz  # PyMuPDF library
from langchain.llms import OpenAI

# Function to extract text from PDF file
def extract_text_from_pdf(file):
    pdf_text = ""
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pdf_text += page.get_text()
    except Exception as e:
        st.error(f"Error: Unable to read the PDF file. {e}")
    return pdf_text

# Function to summarize a chunk of text
def summarize_chunk(chunk, openai_api_key):
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)
    prompt = f"Please summarize the following text:\n\n{chunk}"
    summary = llm(prompt)
    return summary

# Function to divide text into chunks of approximately 2000 tokens
def chunk_text(text, chunk_size=2000):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Function to generate response using ChatGPT based on PDF content
def generate_response(input_text, pdf_text, openai_api_key):
    chunks = chunk_text(pdf_text)
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)
    response = ""
    for chunk in chunks:
        prompt = f"Based on the following document:\n\n{chunk}\n\nAnswer the following question:\n\n{input_text}"
        response_chunk = llm(prompt)
        response += response_chunk + "\n"
        if input_text.lower() in response_chunk.lower():
            break
    return response

# Sidebar - Input OpenAI API key
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
st.sidebar.write("Do you want to get your OpenAI API key?")
st.sidebar.markdown("[Get a free OpenAI API key](https://gptforwork.com/help/knowledge-base/create-openai-api-key)")

st.title('🦜Doc4Chat')
st.info("Discover answers instantly with Doc4Chat, your personal knowledge assistant!")

# Sidebar - Dropdown menu with instructions
with st.sidebar.expander("Instructions"):
    st.write("""
    1. **Input your OpenAI API key**: Enter your OpenAI API key in the provided field.
    2. **Upload your knowledge base PDF**: Upload the PDF file containing the information you want to chat about.
    3. **Chat with Neochat**: Type your question in the input box and click 'Ask' to chat with Neochat based on your uploaded knowledge base.
    """)

st.sidebar.markdown("[Powered by Botarmy Hub, chat with us for AI consultancy](https://botarmy-chat.streamlit.app/)")

# Upload PDF file about the topic
uploaded_file = st.file_uploader("Upload PDF file about the topic", type="pdf")

if uploaded_file is not None:
    # Extract text from the uploaded PDF file
    pdf_text = extract_text_from_pdf(uploaded_file)

    st.warning("Welcome to Doc4Chat! Feel free to ask any questions about the topic.")

    user_input = st.text_input("You:", "")

    if st.button("Ask") and user_input:
        if openai_api_key:
            response = generate_response(user_input, pdf_text, openai_api_key)
            st.info(f"Doc4Chat: {response}")
        else:
            st.error("Please enter your OpenAI API key in the sidebar.")
