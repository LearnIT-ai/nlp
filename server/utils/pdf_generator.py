import os
from weasyprint import HTML

class PDFGeneratorHtml:
    def __init__(self, base_dir="static\simple_silabus_generated"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_html_as_pdf(self, html_content: str, filename: str) -> str:
        full_path = os.path.join(self.base_dir, filename)
        HTML(string=html_content).write_pdf(full_path)