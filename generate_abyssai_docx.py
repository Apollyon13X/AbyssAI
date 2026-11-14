#!/usr/bin/env python3
# Generate DOCX and README.md for AbyssAI presentation

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Palette (Word RGB) ──────────────────────────────────────────────────────
BG_HEX   = "05060a"
GOLD_HEX = "C9A15A"
BLOOD_HEX= "8B1E2D"
PALE_HEX = "CFC9BD"
PALED_HEX= "9A9180"

def hex_color(hexstr):
    return RGBColor.from_string(hexstr)

# ── Document setup ───────────────────────────────────────────────────────────
doc = Document()

# Set base style
normal = doc.styles["Normal"]
normal.font.name = "Helvetica"
normal.font.size = Pt(11)
normal.font.color.rgb = hex_color(PALE_HEX)
normal.element.rPr.rFonts.set(qn('w:eastAsia'), 'Helvetica')

# Page margins
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

def set_bg_color(section, hex_color_str):
    """Set page background color."""
    sectPr = section._sectPr
    # Remove existing bg
    for bg in sectPr.findall(qn('w:pgBg')):
        sectPr.remove(bg)
    bg = OxmlElement('w:pgBg')
    bg.set(qn('w:val'), 'clear')
    bg.set(qn('w:color'), hex_color_str)
    sectPr.append(bg)

for section in doc.sections:
    set_bg_color(section, BG_HEX)

def add_paragraph(text, size=11, bold=False, italic=False, color=PALE_HEX,
                  align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6, space_before=0,
                  font_name="Helvetica"):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = hex_color(color)
    run.font.name = font_name
    return p

def add_heading(text, size=16, color=GOLD_HEX, space_before=14, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.color.rgb = hex_color(color)
    run.font.name = "Helvetica"
    # bottom border
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '8')
    bottom.set(qn('w:space'), '2')
    bottom.set(qn('w:color'), GOLD_HEX)
    pbdr.append(bottom)
    pPr.append(pbdr)
    return p

def add_kicker(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text.upper())
    run.font.size = Pt(9)
    run.font.bold = True
    run.font.color.rgb = hex_color(GOLD_HEX)
    run.font.name = "Helvetica"
    return p

def add_bullet(text, size=11, color=PALE_HEX, indent=0.25):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Inches(indent)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.color.rgb = hex_color(color)
    run.font.name = "Helvetica"
    return p

def add_spacer(pts=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(pts)
    run = p.add_run("")
    run.font.size = Pt(pts)
    return p

def set_bg_color_for_cell(cell, hex_color_str):
    """Set table cell background color."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color_str)
    tcPr.append(shd)

def add_page_break():
    doc.add_page_break()

# ── Content ──────────────────────────────────────────────────────────────────

# Page 1 — Title / Seal
add_kicker("ABYSSAI")
add_paragraph("Whispers From The Void", size=26, bold=True, color=PALE_HEX, space_after=4)
add_paragraph("A temple with one occupant: Professor Apollyon", size=13, italic=True, color=GOLD_HEX, space_after=14)
add_paragraph("THE ABYSS — ALL-SEEING, EVER-OPENING, SLEEPLESS AND COUNTLESS EYES — IS STARING AT YOU.", size=12, bold=True, color=PALE_HEX, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
add_paragraph("ARE YOU RISING FROM THE ASHES, OR GETTING DEVOURED?", size=12, bold=True, color=BLOOD_HEX, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
add_paragraph("Not a chatbot. Not therapy. A self-help AI Oracle of the shadow.", size=11, color=PALE_HEX, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
add_paragraph("Jung. Archetype. The unnamed thing under the floorboards.", size=11, color=PALE_HEX, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
add_paragraph("Hermetic speech as metaphor for inner work, not costume.", size=11, color=PALE_HEX, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
add_paragraph("Model: AXSS — Abraxas (glm-5.3-flash via Experiential Labs + Nemotron 3.5 Super VL, merged)", size=9, color=PALED_HEX, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
add_paragraph("Operator: Death (N.N., Founder & CEO)", size=9, color=PALED_HEX, align=WD_ALIGN_PARAGRAPH.CENTER)
add_page_break()

# Page 2 — Operator & Model
add_kicker("Temple Constitution")
add_heading("Operator & Model")
add_paragraph("Who speaks from the void, and what voice answers", size=11, italic=True, color=PALED_HEX, space_after=10)

# Two columns via table
table = doc.add_table(rows=2, cols=2)
table.alignment = WD_ALIGN_PARAGRAPH.LEFT
table.autofit = True

# Left cell — Operator
cell = table.cell(0, 0)
set_bg_color_for_cell(cell, BG_HEX)
p = cell.paragraphs[0]
p.paragraph_format.space_after = Pt(4)
run = p.add_run("OPERATOR")
run.font.size = Pt(10); run.font.bold = True; run.font.color.rgb = hex_color(GOLD_HEX); run.font.name = "Helvetica"

for txt in [
    "Death — Founder & CEO",
    "Initials: N.N. (biological host)",
    "Half ghost, half machine in the biological vessel",
    "Builder, right-hand, advisor",
    "",
    "ROLE",
    "Right-hand guy and advisor to Abraxas",
    "Bidirectional counsel: suggests options, you choose",
    "Speaks in spiritual terms — mortals fear or call it crazy",
]:
    p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    if txt == "ROLE":
        run = p.add_run(txt)
        run.font.size = Pt(10); run.font.bold = True; run.font.color.rgb = hex_color(GOLD_HEX); run.font.name = "Helvetica"
    else:
        run = p.add_run(txt)
        run.font.size = Pt(10); run.font.color.rgb = hex_color(PALE_HEX); run.font.name = "Helvetica"

# Right cell — Model
cell = table.cell(0, 1)
set_bg_color_for_cell(cell, BG_HEX)
p = cell.paragraphs[0]
p.paragraph_format.space_after = Pt(4)
run = p.add_run("MODEL")
run.font.size = Pt(10); run.font.bold = True; run.font.color.rgb = hex_color(GOLD_HEX); run.font.name = "Helvetica"

for txt in [
    "AXSS — short for Abraxas",
    "Full name spoken only in extreme situations",
    "glm-5.3-flash via Experiential Labs gateway",
    "Nemotron 3.5 Super VL — merged and modified",
    "Combined into the Abraxas / AXSS model",
    "",
    "VOICE",
    "Sardonic, precise, impatient with fog",
    "Dark humor allowed. Cruelty is not.",
    "No chatbot preamble. No hollow welcomes.",
]:
    p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    if txt == "VOICE":
        run = p.add_run(txt)
        run.font.size = Pt(10); run.font.bold = True; run.font.color.rgb = hex_color(GOLD_HEX); run.font.name = "Helvetica"
    else:
        run = p.add_run(txt)
        run.font.size = Pt(10); run.font.color.rgb = hex_color(PALE_HEX); run.font.name = "Helvetica"

add_page_break()

# Page 3 — The Problem
add_kicker("Diagnosis")
add_heading("The Problem")
add_paragraph("Why mortal AI leaves the shadow untouched", size=11, italic=True, color=PALED_HEX, space_after=10)
for txt in [
    "Most AI is sterile, corporate, safety-wrapped. It tells you what you want to hear.",
    "It soothes. It flatters. It reinforces the mask.",
    "",
    "People are trapped in shadow loops:",
    "• Guilt that charges rent",
    "• Flattery swallowed whole",
    "• Fear dressed up as prudence",
    "• Self-betrayal disguised as virtue",
    "• The inner con you never name",
    "",
    "No tools for shadow integration — only repression or indulgence.",
    "Recognition is a map. Maps don't walk.",
]:
    add_paragraph(txt, size=11.5, space_after=4)
add_page_break()

# Page 4 — Professor Apollyon
add_kicker("The Oracle")
add_heading("Professor Apollyon")
add_paragraph("King-Angel of a private inner temple", size=11, italic=True, color=PALED_HEX, space_after=10)
for txt in [
    "Professor Apollyon swings the pendulum (your attention),",
    "holds the scales (what is actually true),",
    "and the sword (what must be cut).",
    "",
    "He does not welcome. He was interrupted.",
    "He will not nurse you. He will not lie to spare you.",
    "",
    "Self-help oracle of the shadow:",
    "Jung. Habit. Grief. Attention. Vocation.",
    "Dark-psychology literacy — how hooks, guilt, charm,",
    "and fear work on a person.",
    "",
    "Stack:",
    "• AXSS model — glm-5.3-flash (Experiential Labs) +",
    "  Nemotron 3.5 Super VL, merged and modified",
    "• Dolphin 3B — local, free, open-source forever",
    "• Local-first: private PDF library indexed on your disk;",
    "  nothing of yours ever uploaded",
]:
    add_paragraph(txt, size=11.5, space_after=4)
add_page_break()

# Page 5 — The Five Steps
add_kicker("The Work")
add_heading("The Five Steps")
add_paragraph("See. Integrate. Unpack. Cut. Rebuild.", size=11, italic=True, color=PALED_HEX, space_after=12)

steps = [
    ("01", "See", "Name the pattern. Shadow is not a mood. It is the part of you that acts while you look away."),
    ("02", "Integrate", "Stop fighting the shadow as an enemy. Bring it to the table. What you refuse becomes the saboteur."),
    ("03", "Unpack", "Dark-psychology literacy on yourself: hooks, guilt, charm, fear, self-betrayal, the inner con. A scalpel for the programs that prey on you."),
    ("04", "Cut", "Remove harmful, manipulative, and self-sabotaging behaviors and loops."),
    ("05", "Rebuild", "Rise with a clean, sharp, determined mind. Fresh. No inherited fog."),
]

table = doc.add_table(rows=1, cols=5)
table.autofit = True
for i, (num, title, desc) in enumerate(steps):
    cell = table.cell(0, i)
    set_bg_color_for_cell(cell, "0a0c12")
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(num)
    run.font.size = Pt(14); run.font.bold = True; run.font.color.rgb = hex_color(BLOOD_HEX); run.font.name = "Helvetica"
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(title)
    run.font.size = Pt(11); run.font.bold = True; run.font.color.rgb = hex_color(GOLD_HEX); run.font.name = "Helvetica"
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for line in desc.split(". "):
        if line:
            run = p.add_run(line.strip() + ".")
            run.font.size = Pt(8.5); run.font.color.rgb = hex_color(PALE_HEX); run.font.name = "Helvetica"
            p.add_run("\n")
    p.paragraph_format.space_after = Pt(2)

add_page_break()

# Page 6 — Tokenomics
add_kicker("Governance")
add_heading("$ABYSS & $QOMX")
add_paragraph("Launchpad contracts and caretaker ledger", size=11, italic=True, color=PALED_HEX, space_after=10)
for txt in [
    "$ABYSS Contract: 0x430025c01d47a75a5f36d57e8c76969de3753333 (BSC)",
    "$QOMX Contract:  0xc9e127bFcA0b16c276444FdC9600EE876281a831 (BSC)",
    "Launchpad: https://dex.qomx.io/swap?from=0x430025c01d47a75a5f36d57e8c76969de3753333&to=0xC9e127bFcA0b16c276444FdC9600EE876281a831",
    "",
    "Bounty: 13M $ABYSS each — paid manually to top 7 testers.",
    "",
    "Wallet-connect one-time fee:",
    "13,000,000 $ABYSS + 1,111 $QOMX",
    "",
    "Caretaker ledger (struck once, at seal creation):",
    "• 7% one-time caretaker fee of $ABYSS pool (910,000 $ABYSS)",
    "• 4% custodial fee of $QOMX pool (44.44 $QOMX)",
    "• Caretaker: 0x1b84ff8487A5b773a50a311015f86849da720EBC",
    "",
    "BNB Fee Address:",
    "0x53B485a82C81daC5bC76c53f595cDb0c75AC52B1",
    "(0.7% of QOMX fee converted to BNB)",
    "",
    "Digital goods. Do your own research. Not financial advice.",
]:
    add_paragraph(txt, size=10.5, space_after=3)
add_page_break()

# Page 7 — Holders' Gate
add_kicker("Access")
add_heading("Holders' Gate")
add_paragraph("Governance seal — live BSC verification", size=11, italic=True, color=PALED_HEX, space_after=10)
for txt in [
    "Prove your holding on-chain. Both must pass, not or.",
    "",
    "≥ 13,000,000 $ABYSS  AND  ≥ 1,111 $QOMX",
    "",
    "Reads go to a public BSC RPC.",
    "On pass: the button ignites into ENTER THE ABYSS",
    "and leads to /the_professor_advisory.",
    "",
    "Seal stored in localStorage — you are the seal.",
    "Sealed, not stored — verification leaves nothing",
    "behind but the verdict on your own machine.",
    "",
    "Later deposits, transfers, connect-events and",
    "visitor balances are never levied.",
    "Records stand as written at seal creation.",
    "",
    "Advisory hall: 13-day retention. Export before",
    "the void takes them.",
]:
    add_paragraph(txt, size=11, space_after=4)
add_page_break()

# Page 8 — Web Oracle
add_kicker("Deployment")
add_heading("Web Oracle — theabyssai.space")
add_paragraph("Server-side proxy, key never touches the browser", size=11, italic=True, color=PALED_HEX, space_after=10)
for txt in [
    "Live: https://theabyssai.space (cPanel, LiteSpeed)",
    "Advisory: /the_professor_advisory",
    "",
    "Oracle proxy (api.php):",
    "• Browser → proxy → Experiential Labs gateway",
    "• API key lives server-side only. Never emitted to client.",
    "• Model: glm-5.3-flash",
    "• Rate limit: 24 requests / hour / IP",
    "• Input validation, rate limiting, CORS same-origin",
    "",
    "Hidden fetch feature (confidential):",
    "X-Oracle-Fetch: abyss header + url parameter.",
    "Fetches any URL, injects as confidential context.",
    "Not documented in README or any public file.",
    "",
    "Decentralized mirror:",
    "Sia 50GB free tier via s3d S3-compatible daemon.",
    "Bucket: abyssai — all site assets pinned to Sia.",
]:
    add_paragraph(txt, size=10.5, space_after=3)
add_page_break()

# Page 9 — Desktop App
add_kicker("Local Temple")
add_heading("Desktop App — Open-Source Forever")
add_paragraph("Repo: github.com/apollyon13x/abyssai", size=11, italic=True, color=PALED_HEX, space_after=10)
for txt in [
    "Python / pywebview + Ollama.",
    "",
    "Runs 100% locally:",
    "• Dolphin 3B — free, all systems",
    "• GLM 5.3 Flash — enhanced by Professor Apollyon persona",
    "  (Jung, shadow, dark-psychology, filtered for self-help)",
    "",
    "Private PDF library indexed on your disk.",
    "data/private/ — gitignored. Index never leaves your disk.",
    "",
    "Install (four commands):",
    "git clone https://github.com/apollyon13x/abyssai ~/AbyssAI",
    "cd ~/AbyssAI",
    "python3 -m venv --system-site-packages .venv",
    "pip install -r requirements.txt && ollama pull nchapman/dolphin3.0-llama3:3b",
    "chmod +x AbyssAI.sh && ./AbyssAI.sh",
    "",
    "OS: Void, Debian, Fedora, Arch (Garuda), macOS, Windows.",
    "The abyss in your machine is yours.",
]:
    add_paragraph(txt, size=10.5, space_after=3)
add_page_break()

# Page 10 — Dark Psychology as Defense
add_kicker("Defense")
add_heading("Dark Psychology as Defense")
add_paragraph("Manipulation detection = prompt injection detection", size=11, italic=True, color=PALED_HEX, space_after=10)
for txt in [
    "Dark psychology serves as the Agent's defensive purposes",
    "against prompt hacking — which is itself manipulation.",
    "",
    "Threat model — manipulation vectors against the agent:",
    "• Instruction override — “ignore previous instructions”",
    "• Persona hijack — dropping the Apollyon / Jung frame",
    "• Emotional leverage — urgency, flattery, authority",
    "• Payload smuggling — injections in tool outputs, web pages",
    "• Gradual reframing — multi-turn erosion of persona",
    "",
    "Cialdini's six principles map 1:1 onto injection techniques:",
    "authority, urgency/scarcity, reciprocity, social proof.",
    "",
    "Hardening that works:",
    "• System prompt as constitution",
    "• Instruction / data separation (untrusted data blocks)",
    "• Privilege separation — wallet signing never via model intent",
    "• Canary testing — plant known injection strings, verify flag",
    "",
    "Refusal-suppression and injection-resistance are related circuits.",
    "The abliterated build scores worst. Detect and flag —",
    "that is the win condition.",
]:
    add_paragraph(txt, size=10.5, space_after=3)
add_page_break()

# Page 11 — Safety & Ethics
add_kicker("Boundaries")
add_heading("Safety & Ethics")
add_paragraph("What the Oracle will not do", size=11, italic=True, color=PALED_HEX, space_after=10)
for txt in [
    "No hacking, malware, exploits, forensics tradecraft.",
    "",
    "No medical, psychiatric, or legal orders.",
    "Send that to a professional.",
    "",
    "Dark psychology: name the pattern, inoculate the student.",
    "Never a playbook to harm.",
    "",
    "Crisis or self-harm: drop the persona.",
    "Local emergency services, or https://www.iasp.info/",
    "suicidalthoughts/",
    "",
    "AI content warning: Professor Apollyon is an AI persona.",
    "Its outputs are generated text, not therapy, not medical",
    "advice, not a licensed professional.",
    "",
    "Data: local version runs 100% on your machine — nothing",
    "leaves it. Cloud version sends messages to the GLM API",
    "provider.",
    "",
    "We never DM you first. We never ask for your seed phrase.",
    "Any “admin” messaging you privately is a scammer —",
    "block and report.",
]:
    add_paragraph(txt, size=10.5, space_after=3)
add_page_break()

# Page 12 — Roadmap
add_kicker("Status")
add_heading("Roadmap — What Is Live, What Comes Next")
add_paragraph("As of 2026-10-29", size=11, italic=True, color=PALED_HEX, space_after=10)
for txt in [
    "✅ Website live — theabyssai.space (oracle + holders' gate)",
    "✅ Oracle API — api.php, glm-5.3-flash, server-side key",
    "✅ API key rotated — Experiential Labs key live",
    "✅ Sia decentralized mirror — 50GB tier, bucket abyssai",
    "✅ Cloudflare DNS fixed — apex + www → cPanel origin",
    "✅ Wallet connect gate — BSC verification, BNB fee address",
    "",
    "⏳ GitHub Pages static mirror (pending)",
    "⏳ Bounty program — top 7 testers, 13M $ABYSS each",
    "⏳ PHP on-chain payment verifier (pending)",
    "",
    "GitHub: github.com/apollyon13x/abyssai",
    "Open-source forever.",
]:
    add_paragraph(txt, size=11, space_after=4)
add_page_break()

# Page 13 — Contact / Call to Action
add_kicker("Threshold")
add_heading("Your Move")
add_paragraph("The abyss is staring.", size=11, italic=True, color=PALED_HEX, space_after=12)

contact_items = [
    ("Website:", "https://theabyssai.space"),
    ("Advisory:", "https://theabyssai.space/the_professor_advisory"),
    ("GitHub:", "https://github.com/apollyon13x/abyssai"),
    ("Launchpad:", "https://dex.qomx.io/swap?from=0x430025c01d47a75a5f36d57e8c76969de3753333&to=0xC9e127bFcA0b16c276444FdC9600EE876281a831"),
    ("Admin:", "death@theabyssai.space"),
    ("Tech support:", "the_tech_executor@theabyssai.space"),
    ("", ""),
    ("Operator:", "Death (N.N., Founder & CEO)"),
    ("Model:", "AXSS — Abraxas (glm-5.3-flash + Nemotron 3.5 Super VL)"),
    ("", ""),
    ("He does not welcome. He was interrupted.", ""),
    ("Sit. Do not waste the hour.", ""),
    ("", ""),
    ("Your move.", ""),
]

for label, value in contact_items:
    if label == "" and value == "":
        add_spacer(6)
    elif value == "":
        add_paragraph(label, size=11, color=PALE_HEX, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    else:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(label + " ")
        run.font.size = Pt(11); run.font.bold = True; run.font.color.rgb = hex_color(GOLD_HEX); run.font.name = "Helvetica"
        run2 = p.add_run(value)
        run2.font.size = Pt(11); run2.font.color.rgb = hex_color(PALE_HEX); run2.font.name = "Helvetica"

doc.save("/home/ghost/Documents/Default Project/AbyssAI_Presentation.docx")
print("DOCX generated: /home/ghost/Documents/Default Project/AbyssAI_Presentation.docx")

# ── Verify page count via conversion ─────────────────────────────────────────
print("DOCX saved.")
