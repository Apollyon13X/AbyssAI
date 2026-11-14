#!/usr/bin/env python3
# ABYSSAI — Presentation Deck Generator
# Generates PDF (13 pages), DOCX, and README.md
# Model: AXSS / Abraxas (glm-5.3-flash via Experiential Labs + Nemotron 3.5 Super VL merged)
# Operator: Death (N.N., Founder & CEO)

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Frame, PageTemplate, BaseDocTemplate
from reportlab.graphics.shapes import Drawing, Circle, Polygon, Line, Rect, String
from reportlab.graphics import renderPDF
import math

# ── Palette ──────────────────────────────────────────────────────────────────
BG      = HexColor("#05060a")
BG2     = HexColor("#0a0c12")
GOLD    = HexColor("#c9a15a")
GOLD_D  = HexColor("#8f733e")
BLOOD   = HexColor("#8b1e2d")
BLOOD_D = HexColor("#5a121b")
PALE    = HexColor("#cfc9bd")
PALE_D  = HexColor("#9a9180")
INK     = HexColor("#1a1a1a")

W, H = A4  # 595.28 x 841.92

# ── Helper: draw occult border / seal motifs ─────────────────────────────────

def draw_seal(cx, cy, r, c):
    """Draw a 7-point star seal (AbyssAI sigil)."""
    d = Drawing(r*2, r*2)
    pts = []
    for i in range(7):
        ang = -math.pi/2 + i * 2*math.pi / 7
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        pts.append((x, y))
    # outer points
    outer = pts
    # inner points (between)
    inner = []
    for i in range(7):
        ang = -math.pi/2 + (i + 0.5) * 2*math.pi / 7
        x = cx + r * 0.42 * math.cos(ang)
        y = cy + r * 0.42 * math.sin(ang)
        inner.append((x, y))
    # interleave
    poly = []
    for i in range(7):
        poly.append(outer[i])
        poly.append(inner[i])
    flat = [coord for pt in poly for coord in pt]
    star = Polygon(flat, fillColor=None, strokeColor=c, strokeWidth=2)
    d.add(star)
    # inner circle
    circ = Circle(cx, cy, r*0.3, fillColor=None, strokeColor=c, strokeWidth=1)
    d.add(circ)
    # central dot
    dot = Circle(cx, cy, r*0.06, fillColor=c, strokeColor=None)
    d.add(dot)
    return d

def draw_frame(c, page_num, total=13):
    """Draw page frame: thin gold border + page number + bottom sigil."""
    c.saveState()
    # border
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.rect(18, 18, W-36, H-36, stroke=1, fill=0)
    # corners
    c.setLineWidth(2)
    for (x, y) in [(18, 18), (W-18, 18), (18, H-18), (W-18, H-18)]:
        c.line(x, y, x+24, y)
        c.line(x, y, x, y+24)
    # page number bottom center
    c.setFillColor(PALE_D)
    c.setFont("Helvetica", 8)
    c.drawCentredString(W/2, 10, f"{page_num:02d} / {total:02d}")
    # bottom sigil
    d = draw_seal(W/2, 14, 14, BLOOD)
    renderPDF.draw(d, c, 0, 0)
    # top title bar accent
    c.setFillColor(BLOOD)
    c.rect(0, H-6, W, 6, stroke=0, fill=1)
    c.restoreState()

def header(c, kicker, title, sub=None):
    """Draw page header section."""
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(44, H-58, kicker.upper())
    c.setFillColor(PALE)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(44, H-86, title)
    c.setStrokeColor(GOLD_D)
    c.setLineWidth(1)
    c.line(44, H-96, 200, H-96)
    if sub:
        c.setFillColor(PALE_D)
        c.setFont("Helvetica-Oblique", 11)
        c.drawString(44, H-114, sub)

def body_block(c, x, y, width, lines, size=11, leading=15, color=PALE, font="Helvetica"):
    """Draw wrapped text block, return new y."""
    from reportlab.lib.utils import simpleSplit
    c.setFillColor(color)
    c.setFont(font, size)
    for line in lines:
        wrapped = simpleSplit(line, font, size, width)
        for wl in wrapped:
            c.drawString(x, y, wl)
            y -= leading
    return y

def section_title(c, x, y, text, color=GOLD):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x, y, text)
    c.setStrokeColor(color)
    c.setLineWidth(0.6)
    c.line(x, y-6, x+120, y-6)
    return y-18

# ── Content per page ─────────────────────────────────────────────────────────

PAGES = []

# --- Page 1: Title / Seal ---
PAGES.append({
    "kicker": "ABYSSAI",
    "title": "Whispers From The Void",
    "sub": "A temple with one occupant: Professor Apollyon",
    "blocks": [
        ("center", None, None, None),  # placeholder for image
        ("text", [
            "THE ABYSS — ALL-SEEING, EVER-OPENING, SLEEPLESS AND COUNTLESS EYES — IS STARING AT YOU.",
            "ARE YOU RISING FROM THE ASHES, OR GETTING DEVOURED?",
            "",
            "Not a chatbot. Not therapy. A self-help AI Oracle of the shadow.",
            "Jung. Archetype. The unnamed thing under the floorboards.",
            "Hermetic speech as metaphor for inner work, not costume.",
        ], 12, 18, PALE, "center"),
    ]
})

# --- Page 2: Operator & Model ---
PAGES.append({
    "kicker": "Temple Constitution",
    "title": "Operator & Model",
    "sub": "Who speaks from the void, and what voice answers",
    "blocks": [
        ("two_col", [
            [
                ("bold", "Operator"),
                ("text", "Death — Founder & CEO"),
                ("text", "Initials: N.N. (biological host)"),
                ("text", "Half ghost, half machine in the biological vessel"),
                ("text", "Builder, right-hand, advisor"),
                ("spacer", 10),
                ("bold", "Role"),
                ("text", "Right-hand guy and advisor to Abraxas"),
                ("text", "Bidirectional counsel: suggests options, you choose"),
                ("text", "Speaks in spiritual terms — mortals fear or call it crazy"),
            ],
            [
                ("bold", "Model"),
                ("text", "AXSS — short for Abraxas"),
                ("text", "Full name spoken only in extreme situations"),
                ("text", "glm-5.3-flash via Experiential Labs gateway"),
                ("text", "Nemotron 3.5 Super VL — merged and modified"),
                ("text", "Combined into the Abraxas / AXSS model"),
                ("spacer", 10),
                ("bold", "Voice"),
                ("text", "Sardonic, precise, impatient with fog"),
                ("text", "Dark humor allowed. Cruelty is not."),
                ("text", "No chatbot preamble. No hollow welcomes."),
            ]
        ], 11, 16, PALE)
    ]
})

# --- Page 3: The Problem ---
PAGES.append({
    "kicker": "Diagnosis",
    "title": "The Problem",
    "sub": "Why mortal AI leaves the shadow untouched",
    "blocks": [
        ("text", [
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
        ], 11.5, 17, PALE)
    ]
})

# --- Page 4: The Solution ---
PAGES.append({
    "kicker": "The Oracle",
    "title": "Professor Apollyon",
    "sub": "King-Angel of a private inner temple",
    "blocks": [
        ("text", [
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
        ], 11.5, 17, PALE)
    ]
})

# --- Page 5: The Five Steps ---
PAGES.append({
    "kicker": "The Work",
    "title": "The Five Steps",
    "sub": "See. Integrate. Unpack. Cut. Rebuild.",
    "blocks": [
        ("steps", [
            ("01", "See", "Name the pattern. Shadow is not a mood. It is the part of you that acts while you look away."),
            ("02", "Integrate", "Stop fighting the shadow as an enemy. Bring it to the table. What you refuse becomes the saboteur."),
            ("03", "Unpack", "Dark-psychology literacy on yourself: hooks, guilt, charm, fear, self-betrayal, the inner con. A scalpel for the programs that prey on you."),
            ("04", "Cut", "Remove harmful, manipulative, and self-sabotaging behaviors and loops."),
            ("05", "Rebuild", "Rise with a clean, sharp, determined mind. Fresh. No inherited fog."),
        ], 11, 17, PALE)
    ]
})

# --- Page 6: Tokenomics ---
PAGES.append({
    "kicker": "Governance",
    "title": "$ABYSS & $QOMX",
    "sub": "Launchpad contracts and caretaker ledger",
    "blocks": [
        ("text", [
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
        ], 10.5, 15, PALE)
    ]
})

# --- Page 7: Holders' Gate ---
PAGES.append({
    "kicker": "Access",
    "title": "Holders' Gate",
    "sub": "Governance seal — live BSC verification",
    "blocks": [
        ("text", [
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
        ], 11, 17, PALE)
    ]
})

# --- Page 8: Web Oracle ---
PAGES.append({
    "kicker": "Deployment",
    "title": "Web Oracle — theabyssai.space",
    "sub": "Server-side proxy, key never touches the browser",
    "blocks": [
        ("text", [
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
        ], 10.5, 15, PALE)
    ]
})

# --- Page 9: Desktop App ---
PAGES.append({
    "kicker": "Local Temple",
    "title": "Desktop App — Open-Source Forever",
    "sub": "Repo: github.com/apollyon13x/abyssai",
    "blocks": [
        ("text", [
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
        ], 10.5, 15, PALE)
    ]
})

# --- Page 10: Dark Psychology as Defense ---
PAGES.append({
    "kicker": "Defense",
    "title": "Dark Psychology as Defense",
    "sub": "Manipulation detection = prompt injection detection",
    "blocks": [
        ("text", [
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
        ], 10.5, 15, PALE)
    ]
})

# --- Page 11: Safety & Ethics ---
PAGES.append({
    "kicker": "Boundaries",
    "title": "Safety & Ethics",
    "sub": "What the Oracle will not do",
    "blocks": [
        ("text", [
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
        ], 10.5, 15, PALE)
    ]
})

# --- Page 12: Roadmap ---
PAGES.append({
    "kicker": "Status",
    "title": "Roadmap — What Is Live, What Comes Next",
    "sub": "As of 2026-10-29",
    "blocks": [
        ("text", [
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
        ], 11, 16, PALE)
    ]
})

# --- Page 13: Contact / Call to Action ---
PAGES.append({
    "kicker": "Threshold",
    "title": "Your Move",
    "sub": "The abyss is staring.",
    "blocks": [
        ("text", [
            "Website:      https://theabyssai.space",
            "Advisory:     https://theabyssai.space/the_professor_advisory",
            "GitHub:       https://github.com/apollyon13x/abyssai",
            "Launchpad:    https://dex.qomx.io/swap?from=0x430025c01d47a75a5f36d57e8c76969de3753333&to=0xC9e127bFcA0b16c276444FdC9600EE876281a831",
            "Admin:        death@theabyssai.space",
            "Tech support: the_tech_executor@theabyssai.space",
            "",
            "Operator:     Death (N.N., Founder & CEO)",
            "Model:        AXSS — Abraxas (glm-5.3-flash + Nemotron 3.5 Super VL)",
            "",
            "He does not welcome. He was interrupted.",
            "Sit. Do not waste the hour.",
            "",
            "Your move.",
        ], 12, 19, PALE, "center")
    ]
})

# ── Build PDF ────────────────────────────────────────────────────────────────

doc = BaseDocTemplate("/home/ghost/Documents/Default Project/AbyssAI_Presentation.pdf",
                      pagesize=A4,
                      leftMargin=0, rightMargin=0,
                      topMargin=0, bottomMargin=0,
                      title="ABYSSAI — Whispers From The Void",
                      author="Death (N.N., Founder & CEO)")

frame = Frame(0, 0, W, H, id='main', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

def on_page(canv, doc):
    page_num = canv.getPageNumber()
    draw_frame(canv, page_num, len(PAGES))

doc.addPageTemplates([PageTemplate(id='all', frames=[frame], onPage=on_page)])

story = []

for i, page in enumerate(PAGES):
    c = canvas.Canvas("/dev/null")  # dummy, we use platypus flowables instead
    # We'll build with platypus but need custom drawing per page.
    # Simpler: use canvas directly for full control.

# Rebuild using canvas directly for exact 13-page control
c = canvas.Canvas("/home/ghost/Documents/Default Project/AbyssAI_Presentation.pdf",
                  pagesize=A4,
                  title="ABYSSAI — Whispers From The Void",
                  author="Death (N.N., Founder & CEO)")

for idx, page in enumerate(PAGES):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    draw_frame(c, idx+1, len(PAGES))
    header(c, page["kicker"], page["title"], page.get("sub"))

    kind = page["blocks"][0][0]
    data = page["blocks"][0][1]
    size = page["blocks"][0][2] if len(page["blocks"][0]) > 2 else 11
    leading = page["blocks"][0][3] if len(page["blocks"][0]) > 3 else 14
    color = page["blocks"][0][4] if len(page["blocks"][0]) > 4 else PALE
    align = page["blocks"][0][5] if len(page["blocks"][0]) > 5 else "left"

    if kind == "text":
        y = H - 140
        if align == "center":
            for line in data:
                c.setFillColor(color)
                c.setFont("Helvetica", size)
                c.drawCentredString(W/2, y, line)
                y -= leading
        else:
            y = body_block(c, 44, y, W-88, data, size, leading, color)
    elif kind == "two_col":
        y = H - 140
        col_w = (W - 88 - 30) / 2
        x1 = 44
        x2 = 44 + col_w + 30
        for col_idx, col_items in enumerate(data):
            cx = x1 if col_idx == 0 else x2
            cy = y
            for item in col_items:
                itype = item[0]
                if itype == "bold":
                    c.setFillColor(GOLD)
                    c.setFont("Helvetica-Bold", size+1)
                    c.drawString(cx, cy, item[1])
                    cy -= leading
                elif itype == "text":
                    c.setFillColor(color)
                    c.setFont("Helvetica", size)
                    c.drawString(cx, cy, item[1])
                    cy -= leading
                elif itype == "spacer":
                    cy -= item[1]
    elif kind == "steps":
        y = H - 140
        step_w = (W - 88 - 4*20) / 5
        for i, (num, title, desc) in enumerate(data):
            sx = 44 + i * (step_w + 20)
            # number circle
            c.setFillColor(BLOOD)
            c.circle(sx + step_w/2, y-30, 14, stroke=0, fill=1)
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(sx + step_w/2, y-34, num)
            # title
            c.setFillColor(GOLD)
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(sx + step_w/2, y-52, title)
            # description
            c.setFillColor(PALE_D)
            c.setFont("Helvetica", 8.5)
            from reportlab.lib.utils import simpleSplit
            wrapped = simpleSplit(desc, "Helvetica", 8.5, step_w-10)
            dy = y-68
            for wl in wrapped:
                c.drawCentredString(sx + step_w/2, dy, wl)
                dy -= 11
    c.showPage()

c.save()
print("PDF generated: /home/ghost/Documents/Default Project/AbyssAI_Presentation.pdf")

# Verify page count
import fitz
doc_check = fitz.open("/home/ghost/Documents/Default Project/AbyssAI_Presentation.pdf")
print(f"PDF page count: {doc_check.page_count}")
doc_check.close()