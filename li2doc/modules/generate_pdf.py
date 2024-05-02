from fpdf import FPDF
from constants import (
    DOC_FILENAME,
)

def generate_pdf(response: str) -> None:
    print("> Generate document from response")
    format_response = response.encode('latin-1', 'replace').decode('latin-1')
    pdf = FPDF('P', 'mm', 'A4')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('helvetica', size=24, style='b')
    pdf.image('./li2doc/assets/raisga-logo.png', 10, 8, 33)
    pdf.ln(30)
    pdf.cell(ln=1, txt=u'~ [li2doc] Generated PDF Document ~', border=0)
    pdf.ln(10)
    pdf.set_font('helvetica', size=12, style='i')
    pdf.multi_cell(ln=1, h=5.0, align='L', w=0, txt=format_response, border=0)
    pdf.output(DOC_FILENAME)
    return None