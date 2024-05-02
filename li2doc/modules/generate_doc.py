from fpdf import FPDF
from constants import (
    DOC_FILENAME,
)

def generate_doc(response: str) -> None:
    print("> Generate document from response")
    format_response = response.encode('latin-1', 'replace').decode('latin-1')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('helvetica', size=12)
    pdf.cell(text=format_response)
    pdf.output(DOC_FILENAME)
    return None