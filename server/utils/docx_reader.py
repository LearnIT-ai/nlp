from docx import Document

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

docx_file = "uk.docx"
docx_text = extract_text_from_docx(docx_file)

print("VALUE .docx file:\n", docx_text)
