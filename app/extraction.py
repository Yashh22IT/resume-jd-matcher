import pdfplumber
import docx

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_path):
    document = docx.Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

if __name__ == "__main__":
    result = extract_text_from_pdf("myresume.pdf")
    print(result)

    result2 = extract_text_from_docx("myresume.docx")
    print(result2)