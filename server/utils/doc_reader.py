import win32com.client
import os

def extract_text_from_doc(doc_path):
    word = win32com.client.Dispatch("Word.Application")
    doc = word.Documents.Open(doc_path)
    text = doc.Content.Text
    doc.Close()
    word.Quit()
    return text.strip()

current_directory = os.path.dirname(os.path.realpath(__file__))

doc_file = os.path.join(current_directory, "doc_file.doc")

doc_text = extract_text_from_doc(doc_file)

print("VALUE .doc file:\n", doc_text)
