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

st.set_page_config(page_title="Doc4Chat", page_icon="🦜")

# Sidebar - Input OpenAI API key
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
st.sidebar.write("Do you want to get your OpenAI API key?")
st.sidebar.markdown("[Get a free OpenAI API key](https://gptforwork.com/help/knowledge-base/create-openai-api-key)")

st.markdown(
        f"""
        <style>
        .stApp {{
            background: url({'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIAJQBDgMBEQACEQEDEQH/xAAcAAEAAgMBAQEAAAAAAAAAAAABAAIDBAUIBgf/xAAqEAACAgEEAgEDBAMBAAAAAAAAAQIDEQQSITEFYUETIlEUMoGhkbHRcf/EABoBAQADAQEBAAAAAAAAAAAAAAABAgMEBQb/xAAhEQEBAQEAAgICAwEAAAAAAAAAAQIRAxIhMRNBBCJRBf/aAAwDAQACEQMRAD8A+fdUDj9q25FJURJ9j1Uel3Pge6PVito2LAm+ly0ba8M2lZ2MEo4L9QxtEoVaAqwKsIVYAwKsAYSqBVgAFQBgDAH0QAkVAgAQAAQABGAAAEAgAwP0uVXo4fZ1cY/pP8k+xxnopaTZlrcXkY9Vt6aLYqNRz7aF2jebZXLStqx8Gk0zuWvKBfqOKSjhFpUMMiUKsIVYAwKsAYSqBVgAFQBgDAH0QAkVAgAQAAQABGAAAEAgAwP1uynDxg8mad/FYadykkkLvkTMt96X6enTaOaeTumnryOJq4Zm8dHbi/DDUakk0+jWKKOlWcJcj34evWtdp1HOUaTfWdzxzrljo2yzrXfRoqowKsIDAqwBhKoFWAAVAGAMAfRACRUCABAABAAEYAAAQCADA/drvHvf0z56eR6vGbReNbmsrtmfl83ItMr+WpVcXFdLgp4L29W1Ph8xfVmXR6Oa59Rg/SSm+i/5OKeq06FQuufkr7+y1zxztVifRvhlpyL62mzpzWFjTkjWVRiZZCrCAwKsAYSqBVgAFQBgDAH0QAkVAgAQAAQABGAAAEAgAwPRtlU/qYyz5Sb5Hs8dfQ6f6dW6XLOPyeS2ork+VrhdJpdo6vDeRNcR+NlKX7eDq/NJFfXrNPRR01blL92DL8t1U+sj57yEnlpHf4p8MNuPPiR1z6YWNbUQTWTTNU1HNuhhs3lZWNeSLxViZIGEKsAYSqBVgAFQBgDAH0QAkVAgAQAAQABGAAAEAgAwPU1emzfyv6PiLv8Aq9m1u3JQp6MJbdM5e1xJ6SV1zeOMnZPJ6xq3Y6SuurdNfcjC+S6vwT7fM+bm3KWDv8GUar5fUxbZ6OK565t0MHTms7Gvt3JxZbvypz4c/U14yb5vWWo0JrBtGdYpFkKsIVYAwlUCrAAKgDAGAPogBIqBAAgAAgACMAAAIBABgeu6qvuzg+F8ebvT0NbV1MN/2/BTVk1eLYvIpGlVxy0Re37W9u/DkeU1HxA38OG2Z8OFqqnfW3j7juxfVFcS/RTeXjC/J058k/TO565mpphDPO5nRjXWdjmXS56OnLKtPVR4ya4Z6cu1YydEY1gkiyqjJQqwBhKoFWAAVAGAMAfRACRUCABAABAAEYAAAQCADA9kKtwr65Pls/xdeHwW2fNdHt2sTr2x3S7OSeD8effa/t34jT1TcuEc1129dGJxzrNC55cuPbNJ5P8AGvvGjdGih4eJS/o2l1pL57y1rlJpcJfHwdviz8K187qlyzuxGOnLvR05ZVr3LNZfP2pXKvXZ0ZY1rSNFGNkirCAwlUCrAAKgDAGAPogBIqBAAgAAgACMAAAIBABge03FYKaxLPmLdauohzlvg+a/6Xg5r21eRtitG2UY9cnkclvw6My1y9bfZLKXXo2xmOnOZHD1Clubw8nXji1cvycOM45OnxVSxwNTHs7M1jqOXevR0YrKtafNbNJ9qX6crULs6Msa1JGnWbGywqwgMJVAqwACoAwBgD6IASKgQAIAAIAAjAAACAQAYHtUmpaup245yeB/1Ljn9o1w0bNns+etz3+rpz7NO6VKzuRMmm+fZy9VPT84S/ydGJppOuR5OdWOIxOnxzSK+c1lkMvCR34lZ6cXUyTbaOvEYaac39jNf2zrk6ntnTljppyNGbGywqwgMJVAqwACoAwBgD6IASKgQAIAAIAAjAAACAQAYHtF2R/Jzb/lYz+/teZYLrGu1mJ4f8z+Vua5qdjTMatirn08P8Hmb/Hv5y3zbHP1Wl3J4Ms75eOjO3C1elshPno7MeSWNe/DheTbUmn8HZ4uVnXA1L5kdmWWnL1DOnLGta14gzTP2pfpy9Qb5ZVqSNWbGyRVhAYSqBVgAFQBgDAH0QAkVAgAQAAQABGAAAEAgAwPYasytp8PPLbj1tdnr+x9VfskXx5/bPptPp+41dRmOXDo5vWda4+ftoS16i2p5WC88Vv02mRLVU2R5cf5I9NRMy4PlNLVbucXyzs8Xk1Ptaz4fK+Q0koNnpeLySsN5cLURak0/wAndlz1q6l4hg0xPlnpybn2dGWVa0jRRRkoVYAwlUCrAAKgDAGAPogBIqBAAgAAgACMAAAIBABgetPrqNyjlYaPg/X4ep6/A1Nu2KsXx2RidM5Vq1MbFhPkazYt6NDyOldi3w/lGvi3+qvLx85rdW6ntTxg9DHjmojrmT8nNNpv/Jr+CIu2rfr4TWHg0z4rFbuOZfssfB0Z7GN5XJ1qWXjo6/HWOnHtXLOmMK15F4qqyUKsAYSqBVgAFQBgDAH0QAkVAgAQAAQABGAAAEAgAwPTuq1LhZCWe/8Ap8bnHw9mRsfqVbSk/ky9PXRxzPqzotknLCTN/Sbh1tLyMLI7c/HZjfDZUxwfM0qxuUeJf7Ovwa/1Go+V1M3GTT7PTzOufTn2WPPZ0ZzGVrHO91xfPJaY7UXTnX3uWcs2zhldNKxp/JrIzta8i6qjJFWEBhKoFWAAVAGAMAfRACRUCABAABAAEYAAAQCADA9Gam2pqLcnw38nymMV7HRTr4RzFDXi6daXk9W5xUl8cM18WeIv05UdbOEsp4Oi+KWKezY/XK2OJPkw/F61f3lcbyUVLMl2dnirHTkNbeZHXGFaGptznk1xlnqtCyRvIz6wSbLKqNkirAqEBhKoFWAAVAGAMAfRACRUCABAABAAEYAAAQCADA/bb9TmP8nhZxOvUumvHU7ZZLXER7GzUbk9z7RWY4XTl228tNnRMsrWH9Q03hsv+OU9mWN++H3FPXl+D265uts5eDo8cZarkXT5Z1ZjCtWTLqsciRVhAYFWAMJVAqwACoAwBgD6IASKgQAIAAIAAjAAACAQAYH6xZdlNZ+Ty5l22sEri3qdVlqOOyfRHWvbKU+UWk4i1ik1HllpOq2te3UtcJl5hX2atl+5YZeZ4rdNO3s0ypWvJmiqrCFWAMCrAGEqgVYABUAYAwB9EAJFQIAEAAEAARgAABAIAMD9Kk3z2cPI6lH/AOko6q5Qj8jh1hs1GOi0wrdNO29s1mVbpq2Tb+TSZU6wuTLcR1SUsjiGORKFWBVgDAqwBhKoFWAAVAGAMAfRACRUCAAAQBAAEYAAAQCADA/QnZL8nNyNu1inOWOy3IdYJzkTIr1gnJlpFesDbZeRDGyUMbJFewBoCriggbUAbUAOC9gVcUEhxXsCrgn+QK7UAbUBVxQBgAwQDagJsXskGxewDYvYBsXshKbF7CBsXsA2L2BNi9gV2L2BNi9gTagBwXsD/9k='}) no-repeat center center fixed;
            background-size: {'cover'};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.title('🦜 :red[Doc4Chat:] Interact with Your PDFs in a Conversational Way')
st.subheader('Load your PDF, ask questions, and receive answers directly from the document.')

# Sidebar - Dropdown menu with instructions
with st.sidebar.expander("Instructions"):
    st.write("""
    1. **Input your OpenAI API key**: Enter your OpenAI API key in the provided field.
    2. **Upload your knowledge base PDF**: Upload the PDF file containing the information you want to chat about.
    3. **Chat with Doc4Chatt**: Type your question in the input box and click 'Ask' to chat with Doc4Chat based on your uploaded knowledge base.
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
