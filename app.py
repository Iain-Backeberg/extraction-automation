import streamlit as st
import pytesseract
from PIL import Image
import pdfplumber
import tempfile
import os
import re

st.set_page_config(page_title="IBAI Document Automation Demonstration", page_icon="📄", layout="wide")
col_logo, col_title = st.columns([0.08, 0.92])  # narrower logo column

with col_logo:
    st.image("logo.png", width=71)  # adjust width as needed

with col_title:
    st.markdown("<h1 style='margin-bottom: 0;text-align: left;'>IBAI Document Automation Demonstration</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    h2 {
        color: #393939;
    }
    h4 {
        color: #ff8c00;
    }
    h6 {
        color: #999999;
    }
    button {
        border-radius: 25px !important;
        background-color: #ff8c00 !important;
        color: #ffffff !important;
        border: 1px solid #ff8c00 !important;
    }
    button:hover {
        background-color: #ffffff !important;
        color: #ff8c00 !important;
        border: 1px solid #ff8c00 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<p style='font-size: 15px;'><b>Why I’m doing this demo:</b>
PDFs, images and scans trap data. This demo showcases that, with just a few clicks, you can speed up wokflow processes by extracting accurate data into your systems automatically.
Manual data-entry takes a lot of time and can lead to mistakes.
Doing it this way can free up time to focus on what really matters in your business - your customers!”
 </p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload PNG/JPG/JPEG/PDF, extract text, edit it, and download as a text file immediately.", type=["png", "jpg", "jpeg", "pdf"])

extracted_text = ""

if uploaded_file is not None:
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)

    # Save uploaded file to temp directory
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    file_ext = os.path.splitext(uploaded_file.name)[1].lower()

    col1, col2 = st.columns(2)

    if file_ext in ['.png', '.jpg', '.jpeg']:
        image = Image.open(temp_file_path)
        with col1:
            st.image(image, caption=uploaded_file.name, use_column_width=True)
        extracted_text = pytesseract.image_to_string(image)
    elif file_ext == '.pdf':
        with pdfplumber.open(temp_file_path) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
            extracted_text = text
    else:
        st.error("Unsupported file type.")
    # Add here:
    extracted_text = re.sub(r'\(cid:\d+\)', '', extracted_text)
    with col1:
        st.subheader("Original Extracted Text (View Only)")
        st.text_area(
            "View extracted text:",
            value=extracted_text,
            height=300,
            key="view_only_text",
            disabled=True
        )

    with col2:
        st.subheader("📝 Edit Extracted Text")
        edited_text = st.text_area("Edit extracted text below:", value=extracted_text, height=300)

        # Prepare text file for download
        text_bytes = edited_text.encode('utf-8')
        st.download_button(
            label="Download extracted text as .txt",
            data=text_bytes,
            file_name="extracted_text.txt",
            mime="text/plain"
        )

    os.remove(temp_file_path)

# Add thin grey line and disclaimer below
st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

st.markdown("""
<p style='font-size: 11px;'><b>Disclaimer:</b>
This demo showcases a proof of concept for document automation.
You can download your extracted text as a plain text (.txt) file for simplicity.
Real-world application requires advanced, paid tools which will handle document processing with a higher degree of accuracy. 
No personal or private information is stored on any servers. All files are temporary, and the final version is downloaded to your personal device.
All production-ready solutions will be tailored to your specific requirements. </p><p style='text-align:center;font-size: 11px;'>Copyright IBAI 2025</p>
""", unsafe_allow_html=True)
