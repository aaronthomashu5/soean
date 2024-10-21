import streamlit as st
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import utils
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

# Configure API key
GOOGLE_GENAI_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_GENAI_API_KEY)


def generate_notes(files, prompt):
    """Generate notes using Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-pro-002')
    
    file_parts = [
        {"mime_type": file.type, "data": file.getvalue()}
        for file in files
    ]
    
    response = model.generate_content([*file_parts, prompt])
    
    return response.text

def create_pdf(content):
    """Create a simple PDF from plain text with line wrapping."""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Use a default font that supports Unicode
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    p.setFont('DejaVuSans', 12)
    
    margin_x = 40
    margin_y = 40
    line_height = 15
    max_width = width - 2 * margin_x
    
    y = height - margin_y
    
    # Split content by line and then wrap longer lines
    for line in content.split('\n'):
        wrapped_lines = utils.simpleSplit(line, 'DejaVuSans', 12, max_width)
        for wrapped_line in wrapped_lines:
            if y < margin_y + line_height:  # Start a new page if we're near the bottom
                p.showPage()
                p.setFont('DejaVuSans', 12)
                y = height - margin_y
            p.drawString(margin_x, y, wrapped_line)
            y -= line_height
    
    p.showPage()
    p.save()
    
    return buffer.getvalue()
    
def main():
    st.title("Engineering Note Generator")
    
    uploaded_files = st.file_uploader("Upload documents", accept_multiple_files=True)
    
    prompt = st.text_area("Enter the answer scheme and prompt:")
    
    if st.button("Generate Notes") and uploaded_files and prompt:
        with st.spinner("Generating notes..."):
            generated_content = generate_notes(uploaded_files, prompt)
        
        st.subheader("Generated Notes:")
        st.write(generated_content)
        
        pdf = create_pdf(generated_content)
        st.download_button(
            label="Download PDF",
            data=pdf,
            file_name="engineering_notes.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
