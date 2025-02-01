import fitz 

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()

pdf_file = "example.pdf"
pdf_text = extract_text_from_pdf(pdf_file)

print("VALUE PDF:\n", pdf_text)
