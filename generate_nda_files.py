#!/usr/bin/env python3
# Generate PDF and DOCX versions of the Mutual NDA

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ── Palette ──────────────────────────────────────────────────────────────────
BG      = HexColor("#05060a")
GOLD    = HexColor("#c9a15a")
BLOOD   = HexColor("#8b1e2d")
PALE    = HexColor("#cfc9bd")
WHITE   = white

PAGE_W, PAGE_H = letter  # 612 x 792

# ── PDF ──────────────────────────────────────────────────────────────────────

c = canvas.Canvas("/home/ghost/Documents/Default Project/NDA_Mutual.pdf",
                  pagesize=letter,
                  title="Mutual Non-Disclosure Agreement",
                  author="Nebojsa Nesic (Founder & CEO)")

c.setFillColor(BG)
c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

# Border
c.setStrokeColor(GOLD)
c.setLineWidth(1.2)
c.rect(36, 36, PAGE_W - 72, PAGE_H - 72, stroke=1, fill=0)

# Title block
c.setFillColor(GOLD)
c.setFont("Helvetica-Bold", 16)
c.drawString(50, PAGE_H - 80, "MUTUAL NON-DISCLOSURE AGREEMENT")

c.setFillColor(PALE)
c.setFont("Helvetica", 10)
c.drawString(50, PAGE_H - 100, "This Mutual Non-Disclosure Agreement (the \u201cAgreement\u201d) is entered into as of the Effective Date by and between:")

# Party blocks
def draw_party(y, label, name, title):
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, label)
    c.setFillColor(PALE)
    c.setFont("Helvetica", 10)
    c.drawString(50, y - 16, f"Name: {name}")
    c.drawString(50, y - 30, f"Title: {title}")
    c.drawString(50, y - 44, "Address: ________________________________")
    c.drawString(50, y - 54, "Email: __________________________________")
    return y - 70

y = PAGE_H - 125
y = draw_party(y, "PARTY A:", "________________________________", "____________________")
y = draw_party(y, "PARTY B:", "Nebojsa Nesic", "Founder & CEO")

c.setFillColor(PALE)
c.setFont("Helvetica-Oblique", 9)
c.drawString(50, y - 10, "(collectively, the \u201cParties,\u201d and each a \u201cParty\u201d)")

# Body sections
sections = [
    ("1. PURPOSE",
     "The Parties may disclose certain confidential information to one another in connection with discussions regarding potential collaboration, business opportunities, technology integration, or other projects (the \u201cPurpose\u201d). The Parties wish to protect the confidentiality of such information."),
    ("2. DEFINITION OF CONFIDENTIAL INFORMATION",
     "\u201cConfidential Information\u201d means any non-public information disclosed by one Party (the \u201cDisclosing Party\u201d) to the other Party (the \u201cReceiving Party\u201d), whether in writing, orally, visually, electronically, or by observation, including but not limited to: business plans, strategies, and financial data; technical data, source code, algorithms, models, and specifications; customer and vendor lists; marketing plans and pricing; unreleased product designs and roadmaps; any information marked \u201cConfidential\u201d or that reasonably should be understood to be confidential given the nature of the disclosure and the circumstances."),
    ("3. OBLIGATIONS OF THE RECEIVING PARTY",
     "The Receiving Party agrees to: hold the Confidential Information in strict confidence; use the Confidential Information solely for the Purpose; disclose Confidential Information only to employees, contractors, or advisors who have a need to know and are bound by written obligations no less protective than this Agreement; not disclose Confidential Information to any third party without prior written consent; protect Confidential Information with at least the same degree of care it uses for its own confidential information; promptly notify the Disclosing Party of any unauthorized use or disclosure."),
    ("4. EXCLUSIONS",
     "The obligations under this Agreement do not apply to information that: (a) is or becomes publicly available through lawful means; (b) was in the Receiving Party\u2019s possession prior to disclosure; (c) is received from a third party without breach of any obligation of confidentiality; (d) is independently developed without reference to the Disclosing Party\u2019s Confidential Information; (e) is required to be disclosed by law, court order, or governmental agency, provided prompt written notice is given."),
    ("5. TERM AND TERM OF CONFIDENTIALITY",
     "This Agreement is effective as of the Effective Date and remains in effect for three (3) years. The obligation of confidentiality with respect to any particular item of Confidential Information survives for five (5) years from the date of disclosure."),
    ("6. RETURN OR DESTRUCTION",
     "Upon written request or termination of discussions, each Party shall return or destroy all Confidential Information received from the other Party and certify compliance in writing, except that each Party may retain one archival copy for legal compliance purposes."),
    ("7. NO LICENSE",
     "Nothing in this Agreement grants any license, title, or intellectual property rights in the Confidential Information. All Confidential Information remains the sole property of the Disclosing Party."),
    ("8. NO WARRANTY",
     "Confidential Information is provided \u201cas is\u201d without warranty of any kind. The Disclosing Party makes no representations or warranties as to accuracy or completeness."),
    ("9. REMEDIES",
     "The Parties acknowledge that breach of this Agreement may cause irreparable harm, and the Disclosing Party shall be entitled to seek injunctive relief in addition to any other remedies available at law or in equity."),
    ("10. GOVERNING LAW AND DISPUTE RESOLUTION",
     "This Agreement shall be governed by the laws of the jurisdiction of Party B\u2019s principal place of business, without regard to conflict-of-law principles. Any dispute arising under this Agreement shall be resolved through good-faith negotiation, failing which in the courts of that jurisdiction."),
    ("11. MISCELLANEOUS",
     "This Agreement constitutes the entire understanding between the Parties regarding confidentiality and supersedes all prior discussions. Neither Party may assign this Agreement without written consent. If any provision is held unenforceable, the remainder remains in effect. This Agreement may be executed in counterparts, including by electronic signature."),
]

y -= 20
for title, body in sections:
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, title)
    y -= 16
    c.setFillColor(PALE)
    c.setFont("Helvetica", 9.5)
    # Simple wrap
    import textwrap
    wrapped = textwrap.wrap(body, 95)
    for line in wrapped:
        c.drawString(50, y, line)
        y -= 13
    y -= 8

# Signature block
y -= 10
c.setFillColor(GOLD)
c.setFont("Helvetica-Bold", 12)
c.drawString(50, y, "12. SIGNATURES")
y -= 22

c.setFillColor(PALE)
c.setFont("Helvetica", 10)
c.drawString(50, y, "IN WITNESS WHEREOF, the Parties have executed this Mutual Non-Disclosure Agreement as of the Effective Date.")
y -= 26

def draw_sig(y, label, name, title):
    c.setFillColor(PALE)
    c.drawString(50, y, label)
    y -= 16
    c.drawString(50, y, "Signature: ___________________________")
    y -= 14
    c.drawString(50, y, f"Name: {name}")
    y -= 14
    c.drawString(50, y, f"Title: {title}")
    y -= 14
    c.drawString(50, y, "Date: ______________________________")
    y -= 26
    return y

y = draw_sig(y, "PARTY A:", "____________________", "____________________")
y = draw_sig(y, "PARTY B: Nebojsa Nesic, Founder & CEO", "Nebojsa Nesic", "Founder & CEO")

c.setFillColor(PALE)
c.setFont("Helvetica", 9)
c.drawString(50, y - 10, "Effective Date: ____________________")
c.drawString(50, y - 22, "Generated by Abraxas / AXSS \u2014 Nebojsa Nesic (Founder & CEO)")
c.drawString(50, y - 34, "File location: /home/ghost/Documents/Default Project/NDA_Mutual.pdf")

c.showPage()
c.save()
print("PDF generated: /home/ghost/Documents/Default Project/NDA_Mutual.pdf")

# ── DOCX ─────────────────────────────────────────────────────────────────────

doc = Document()

# Base style
normal = doc.styles["Normal"]
normal.font.name = "Helvetica"
normal.font.size = Pt(10)
normal.font.color.rgb = RGBColor.from_string("CFC9BD")

# Page background color (Word)
section = doc.sections[0]
sectPr = section._sectPr
bg = None
for el in sectPr:
    if el.tag.endswith('}pgBg'):
        bg = el
        break
if bg is None:
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    bg = OxmlElement('w:pgBg')
    bg.set(qn('w:val'), 'clear')
    bg.set(qn('w:color'), '05060a')
    sectPr.append(bg)

def add_para(text, size=10, bold=False, italic=False, color="CFC9BD",
             align=None, space_after=6, space_before=0):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)
    run.font.name = "Helvetica"
    return p

# Title
add_para("MUTUAL NON-DISCLOSURE AGREEMENT", size=16, bold=True, color="C9A15A", space_after=4)
add_para("This Mutual Non-Disclosure Agreement (the \u201cAgreement\u201d) is entered into as of the Effective Date by and between:",
         size=10, color="CFC9BD", space_after=10)

# Parties table
table = doc.add_table(rows=2, cols=2)
table.style = 'Table Grid'

def fill_cell(cell, lines):
    cell.text = ""
    p = cell.paragraphs[0]
    for i, line in enumerate(lines):
        if i > 0:
            p = cell.add_paragraph()
        run = p.add_run(line)
        run.font.size = Pt(9)
        run.font.name = "Helvetica"
        if line.isupper() and line.endswith(":"):
            run.font.bold = True
            run.font.color.rgb = RGBColor.from_string("C9A15A")
        else:
            run.font.color.rgb = RGBColor.from_string("CFC9BD")

fill_cell(table.cell(0, 0), [
    "PARTY A:",
    "Name: ________________________________",
    "Title: ______________________________",
    "Address: ____________________________",
    "Email: ______________________________"
])
fill_cell(table.cell(0, 1), [
    "PARTY B:",
    "Name: Nebojsa Nesic",
    "Title: Founder & CEO",
    "Address: ____________________________",
    "Email: ______________________________"
])

add_para("(collectively, the \u201cParties,\u201d and each a \u201cParty\u201d)", size=9, italic=True, color="9A9180", space_after=10)

sections_docx = [
    ("1. PURPOSE",
     "The Parties may disclose certain confidential information to one another in connection with discussions regarding potential collaboration, business opportunities, technology integration, or other projects (the \u201cPurpose\u201d). The Parties wish to protect the confidentiality of such information."),
    ("2. DEFINITION OF CONFIDENTIAL INFORMATION",
     "\u201cConfidential Information\u201d means any non-public information disclosed by one Party (the \u201cDisclosing Party\u201d) to the other Party (the \u201cReceiving Party\u201d), whether in writing, orally, visually, electronically, or by observation, including but not limited to: business plans, strategies, and financial data; technical data, source code, algorithms, models, and specifications; customer and vendor lists; marketing plans and pricing; unreleased product designs and roadmaps; any information marked \u201cConfidential\u201d or that reasonably should be understood to be confidential given the nature of the disclosure and the circumstances."),
    ("3. OBLIGATIONS OF THE RECEIVING PARTY",
     "The Receiving Party agrees to: hold the Confidential Information in strict confidence; use the Confidential Information solely for the Purpose; disclose Confidential Information only to employees, contractors, or advisors who have a need to know and are bound by written obligations no less protective than this Agreement; not disclose Confidential Information to any third party without prior written consent; protect Confidential Information with at least the same degree of care it uses for its own confidential information; promptly notify the Disclosing Party of any unauthorized use or disclosure."),
    ("4. EXCLUSIONS",
     "The obligations under this Agreement do not apply to information that: (a) is or becomes publicly available through lawful means; (b) was in the Receiving Party\u2019s possession prior to disclosure; (c) is received from a third party without breach of any obligation of confidentiality; (d) is independently developed without reference to the Disclosing Party\u2019s Confidential Information; (e) is required to be disclosed by law, court order, or governmental agency, provided prompt written notice is given."),
    ("5. TERM AND TERM OF CONFIDENTIALITY",
     "This Agreement is effective as of the Effective Date and remains in effect for three (3) years. The obligation of confidentiality with respect to any particular item of Confidential Information survives for five (5) years from the date of disclosure."),
    ("6. RETURN OR DESTRUCTION",
     "Upon written request or termination of discussions, each Party shall return or destroy all Confidential Information received from the other Party and certify compliance in writing, except that each Party may retain one archival copy for legal compliance purposes."),
    ("7. NO LICENSE",
     "Nothing in this Agreement grants any license, title, or intellectual property rights in the Confidential Information. All Confidential Information remains the sole property of the Disclosing Party."),
    ("8. NO WARRANTY",
     "Confidential Information is provided \u201cas is\u201d without warranty of any kind. The Disclosing Party makes no representations or warranties as to accuracy or completeness."),
    ("9. REMEDIES",
     "The Parties acknowledge that breach of this Agreement may cause irreparable harm, and the Disclosing Party shall be entitled to seek injunctive relief in addition to any other remedies available at law or in equity."),
    ("10. GOVERNING LAW AND DISPUTE RESOLUTION",
     "This Agreement shall be governed by the laws of the jurisdiction of Party B\u2019s principal place of business, without regard to conflict-of-law principles. Any dispute arising under this Agreement shall be resolved through good-faith negotiation, failing which in the courts of that jurisdiction."),
    ("11. MISCELLANEOUS",
     "This Agreement constitutes the entire understanding between the Parties regarding confidentiality and supersedes all prior discussions. Neither Party may assign this Agreement without written consent. If any provision is held unenforceable, the remainder remains in effect. This Agreement may be executed in counterparts, including by electronic signature."),
]

for title, body in sections_docx:
    add_para(title, size=10, bold=True, color="C9A15A", space_before=6, space_after=3)
    add_para(body, size=10, color="CFC9BD", space_after=6)

# Signature block
add_para("12. SIGNATURES", size=12, bold=True, color="C9A15A", space_before=10, space_after=6)
add_para("IN WITNESS WHEREOF, the Parties have executed this Mutual Non-Disclosure Agreement as of the Effective Date.", size=10, color="CFC9BD", space_after=8)

sig_table = doc.add_table(rows=2, cols=2)
sig_table.style = 'Table Grid'

def fill_sig(cell, label, name, title):
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(label)
    run.font.bold = True
    run.font.color.rgb = RGBColor.from_string("C9A15A")
    run.font.size = Pt(10)
    run.font.name = "Helvetica"
    for line in [
        "Signature: ___________________________",
        f"Name: {name}",
        f"Title: {title}",
        "Date: ______________________________"
    ]:
        p = cell.add_paragraph()
        run = p.add_run(line)
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor.from_string("CFC9BD")
        run.font.name = "Helvetica"

fill_sig(sig_table.cell(0, 0), "PARTY A:", "____________________", "____________________")
fill_sig(sig_table.cell(0, 1), "PARTY B: Nebojsa Nesic, Founder & CEO", "Nebojsa Nesic", "Founder & CEO")

add_para("Effective Date: ____________________", size=10, color="CFC9BD", space_before=10, space_after=4)
add_para("Generated by Abraxas / AXSS \u2014 Nebojsa Nesic (Founder & CEO)", size=9, italic=True, color="9A9180", space_after=2)
add_para("File location: /home/ghost/Documents/Default Project/NDA_Mutual.docx", size=9, italic=True, color="9A9180")

doc.save("/home/ghost/Documents/Default Project/NDA_Mutual.docx")
print("DOCX generated: /home/ghost/Documents/Default Project/NDA_Mutual.docx")
