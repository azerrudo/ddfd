from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin   = Inches(1.15)
    section.right_margin  = Inches(1.15)

# ── Colour palette ────────────────────────────────────────────────────────────
NAVY   = RGBColor(0x0D, 0x2B, 0x55)   # headings / rule
SLATE  = RGBColor(0x44, 0x54, 0x6E)   # sub-labels
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT  = RGBColor(0xF0, 0xF4, 0xF8)   # alternate table row
GOLD   = RGBColor(0xC8, 0x9A, 0x2A)   # accent / callout border

# ── Helper: set paragraph shading ─────────────────────────────────────────────
def shade_cell(cell, hex_fill):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_fill)
    tcPr.append(shd)

def set_cell_border(cell, **kwargs):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge, style in kwargs.items():
        tag = OxmlElement(f'w:{edge}')
        for k, v in style.items():
            tag.set(qn(f'w:{k}'), v)
        tcBorders.append(tag)
    tcPr.append(tcBorders)

def no_space_para(para):
    pPr = para._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), '0')
    spacing.set(qn('w:after'),  '0')
    pPr.append(spacing)

# ── Helper: horizontal rule ───────────────────────────────────────────────────
def add_rule(doc, colour_hex='0D2B55', thickness=12):
    p    = doc.add_paragraph()
    no_space_para(p)
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot  = OxmlElement('w:bottom')
    bot.set(qn('w:val'),   'single')
    bot.set(qn('w:sz'),    str(thickness))
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), colour_hex)
    pBdr.append(bot)
    pPr.append(pBdr)
    return p

# ── Helper: styled heading ────────────────────────────────────────────────────
def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text.upper())
    run.bold      = True
    run.font.size = Pt(8.5)
    run.font.color.rgb = NAVY
    run.font.name = 'Calibri'
    # letter spacing via rPr kern — skip, just use caps styling
    return p

# ── Helper: body paragraph ────────────────────────────────────────────────────
def add_body(doc, text, space_before=0, space_after=6, size=11):
    p   = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    run = p.add_run(text)
    run.font.size  = Pt(size)
    run.font.name  = 'Calibri'
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
    return p, run

# ── Helper: table with header row ────────────────────────────────────────────
def make_table(doc, headers, rows, col_widths, alt_shade=True):
    n_cols = len(headers)
    table  = doc.add_table(rows=1 + len(rows), cols=n_cols)
    table.style = 'Table Grid'

    # header row
    hdr = table.rows[0]
    for i, (cell, txt) in enumerate(zip(hdr.cells, headers)):
        shade_cell(cell, '0D2B55')
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p   = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        no_space_para(p)
        run = p.add_run(txt)
        run.bold           = True
        run.font.size      = Pt(8)
        run.font.color.rgb = WHITE
        run.font.name      = 'Calibri'
        cell.width = Inches(col_widths[i])

    # data rows
    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        fill = 'F0F4F8' if (alt_shade and r_idx % 2 == 0) else 'FFFFFF'
        for c_idx, (cell, txt) in enumerate(zip(row.cells, row_data)):
            shade_cell(cell, fill)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p   = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            no_space_para(p)
            run = p.add_run(txt)
            run.font.size      = Pt(8)
            run.font.name      = 'Calibri'
            run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
            cell.width = Inches(col_widths[i])

    return table

def add_insight(doc, text):
    """Gold-left-bordered insight box."""
    p   = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(10)
    p.paragraph_format.left_indent  = Inches(0.2)
    pPr  = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'),   'single')
    left.set(qn('w:sz'),    '18')
    left.set(qn('w:space'), '4')
    left.set(qn('w:color'), 'C89A2A')
    pBdr.append(left)
    pPr.append(pBdr)
    run = p.add_run(text)
    run.italic         = True
    run.font.size      = Pt(9)
    run.font.name      = 'Calibri'
    run.font.color.rgb = SLATE
    return p


# ══════════════════════════════════════════════════════════════════════════════
#  DOCUMENT CONTENT
# ══════════════════════════════════════════════════════════════════════════════

# ── Cover block ───────────────────────────────────────────────────────────────
p = doc.add_paragraph()
no_space_para(p)
p.paragraph_format.space_after = Pt(2)
run = p.add_run('MERIDIAN TECHNOLOGIES')
run.bold           = True
run.font.size      = Pt(22)
run.font.name      = 'Calibri'
run.font.color.rgb = NAVY

p = doc.add_paragraph()
no_space_para(p)
p.paragraph_format.space_after = Pt(2)
run = p.add_run('Annual Board Strategic Review')
run.font.size      = Pt(13)
run.font.name      = 'Calibri'
run.font.color.rgb = SLATE

p = doc.add_paragraph()
no_space_para(p)
p.paragraph_format.space_after = Pt(16)
run = p.add_run('CEO Opening Statement  ·  May 2026  ·  ~5 minutes')
run.font.size      = Pt(10)
run.font.name      = 'Calibri'
run.font.color.rgb = SLATE

add_rule(doc)

# ── Opening ───────────────────────────────────────────────────────────────────
add_section_heading(doc, 'Opening')

add_body(doc,
    'Thank you. Before we move into the prepared agenda, I want to take five '
    'minutes to give you my honest read on where this company stands — not the '
    'investor-relations version, but the CEO version.',
    space_after=6)

add_body(doc,
    'I have been in this role for fifteen months. I have spent time with our '
    'largest customers, our board, and every layer of this organization. What I '
    'want to share today is what I have concluded, what concerns me, and what I '
    'am asking from you.',
    space_after=6)

# ── Where We Stand ────────────────────────────────────────────────────────────
add_section_heading(doc, 'Where We Stand')

add_body(doc,
    'The headline numbers are solid. Full-year 2025 revenue of four hundred '
    'million dollars, up eleven percent. Operating margin of twelve percent, up '
    'from five percent three years ago. Four hundred sixty-three million in cash '
    'and no debt. Free cash flow margin approaching eighteen percent.',
    space_after=6)

add_body(doc,
    'Those numbers deserve acknowledgment. Lenore built a financially disciplined '
    'business, and this team has continued that discipline through a transition '
    'year. I am proud of it.',
    space_after=6)

add_body(doc,
    'And I want to be equally honest about what those numbers conceal. Revenue '
    'growth has decelerated every single year — twenty-eight percent in 2022, '
    'sixteen in 2024, eleven in 2025, and we are guiding ten to fourteen for 2026. '
    'That is not a coincidence. That is a structural pattern, and it is the central '
    'issue this board needs to help me address.',
    space_after=8)

# ── Exhibit 1: Company Snapshot ───────────────────────────────────────────────
add_section_heading(doc, 'Exhibit 1 — Company Financials: Full-Year Snapshot')

make_table(doc,
    headers   = ['Metric', 'FY 2022', 'FY 2023', 'FY 2024', 'FY 2025', '2026 Guide'],
    col_widths= [2.1, 0.82, 0.82, 0.82, 0.82, 0.9],
    rows = [
        ['Revenue ($M)',      '$260',  '$311',  '$360',  '$400',  '$440–455'],
        ['YoY Revenue Growth','—',     '+19%',  '+16%',  '+11%',  '+10–14%'],
        ['ARR ($M)',          '$275',  '$328',  '$375',  '$413',  '—'],
        ['Gross Margin',      '78.0%', '78.6%', '79.2%', '79.6%', '—'],
        ['Operating Margin',  '5.1%',  '7.7%',  '10.0%', '12.4%', '14–15%'],
        ['FCF Margin',        '10.4%', '13.9%', '16.2%', '17.8%', '—'],
        ['Cash ($M)',         '$344',  '$392',  '$432',  '$463',  '—'],
    ]
)

add_insight(doc,
    'Read: Revenue growth decelerates every year as margins expand. The business '
    'is more profitable and slower-growing simultaneously — a pattern that demands '
    'a deliberate strategic answer in 2026.')

# ── Issue 1 ───────────────────────────────────────────────────────────────────
add_section_heading(doc, 'Issue 1 — Growth Deceleration')

add_body(doc,
    'The first issue is growth deceleration, and the segment picture explains it '
    'precisely. We are not one company — we are three businesses in one P&L, and '
    'they are moving in very different directions.',
    space_after=6)

add_section_heading(doc, 'Exhibit 2 — Segment ARR: Three-Year Mix Shift')

make_table(doc,
    headers   = ['Segment', 'ARR Q4 2022', 'Mix', 'ARR Q4 2025', 'Mix', 'YoY Growth', 'NRR', 'Logo Churn'],
    col_widths= [1.1, 0.92, 0.52, 0.92, 0.52, 0.85, 0.62, 0.82],
    rows = [
        ['Enterprise',  '~$74M',  '27%', '~$167M', '40%', '+21%',  '125%', '2.6%'],
        ['Mid-market',  '~$96M',  '35%', '~$194M', '47%', '+6%',   '102%', '10.2%'],
        ['SMB',         '~$105M', '38%', '~$52M',  '13%', '-23%',  '84%',  '22.1%'],
        ['Total',       '~$275M', '100%','~$413M', '100%', '+10%', '109%', '—'],
    ]
)

add_insight(doc,
    'Read: Enterprise has nearly doubled its ARR share (27% → 40%) and is the '
    'engine of the business. SMB has collapsed (38% → 13%) and is an active drag. '
    'Mid-market, at 47% of ARR, is the swing segment — and at 6% growth with NRR '
    'of 102%, it is barely treading water.')

add_body(doc,
    'The SMB decline costs us approximately thirty million dollars of growth '
    'headwind in 2026 alone. I have made the decision to run SMB on a '
    'self-funded basis. The segment will stand on its own economics or we will '
    'manage it down in a controlled way. We will not subsidize it from enterprise '
    'margins.',
    space_after=8)

# ── Issue 2 ───────────────────────────────────────────────────────────────────
add_section_heading(doc, 'Issue 2 — AI Competitive Position')

add_body(doc,
    'The second issue is AI. I will not soften this: we were late. Asana shipped '
    'their agent in the fall of 2024. We shipped AI Copilot to general '
    'availability in September 2025. Asana has since bundled AI into their '
    'standard tier. Monday is now larger than us by ARR. ClearAI Work raised '
    'a hundred-and-twenty-million-dollar round at a billion-dollar valuation and '
    'is taking our SMB.',
    space_after=6)

add_body(doc,
    'And yet — the early Copilot numbers give me genuine confidence that we can '
    'compete. Seven hundred ten paying seats at year-end, against an internal '
    'target of six hundred. A forty-four-percent attach rate on enterprise renewals '
    'in Q4, against a target of forty percent. The Helio Labs acquisition — '
    'twenty-eight engineers from leading AI labs, a working agent framework — '
    'compressed our roadmap by an estimated fifteen months.',
    space_after=6)

add_section_heading(doc, 'Exhibit 3 — AI Copilot Ramp')

make_table(doc,
    headers   = ['Quarter', 'Paying Seats', 'ARR Contribution', 'Enterprise Attach Rate'],
    col_widths= [1.2, 1.2, 1.55, 1.85],
    rows = [
        ['Q4 2024 (closed beta)', '0',   '$0',       '—'],
        ['Q1 2025',               '0',   '$0',       '—'],
        ['Q2 2025 (open beta)',   '140', '~$0.7M',   '—'],
        ['Q3 2025 (GA Sep)',      '420', '~$2.0M',   '—'],
        ['Q4 2025',               '710', '~$3.5M',   '44%  ✓ (target: 40%)'],
    ]
)

add_insight(doc,
    'Read: Copilot is early-stage at $3.5M ARR, but the Q4 attach rate of 44% '
    'is the most important leading indicator in this business. If it holds as the '
    'enterprise renewal base cycles through 2026, AI becomes a material growth '
    'driver — not a cost.')

add_body(doc,
    'I will share the full AI roadmap at Investor Day on March eleventh. What I '
    'will say here is that our enterprise differentiation — FedRAMP Moderate, '
    'HIPAA, the governance and audit features that regulated industries require — '
    'is where we win, and where Asana does not. We will build our AI strategy '
    'around that moat.',
    space_after=8)

# ── Issue 3 ───────────────────────────────────────────────────────────────────
add_section_heading(doc, 'Issue 3 — Organizational Readiness')

add_body(doc,
    'The third issue is internal, and the one I am most focused on. The October '
    'employee survey — eighty-one percent response rate — was candid. '
    'Thirty-one percent of engineering open-ends cited roadmap thrash as their '
    'primary frustration. Nineteen percent of all employees said they cannot '
    'clearly articulate what makes Meridian different from Asana with AI. '
    'Twenty-seven percent of senior engineers said their compensation is not '
    'keeping pace with the market.',
    space_after=6)

add_section_heading(doc, 'Exhibit 4 — Sales Efficiency Trend')

make_table(doc,
    headers   = ['Metric', 'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q4 2025'],
    col_widths= [1.9, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
    rows = [
        ['Magic Number',                  '1.20', '1.16', '1.10', '1.05', '1.02', '0.92'],
        ['CAC Payback (months)',           '18.2', '18.9', '19.5', '20.4', '21.1', '22.4'],
        ['New ARR / Quota Rep ($K)',       '$1,320','$1,290','$1,255','$1,210','$1,180','$1,110'],
        ['NRR — Overall',                 '114%', '113%', '112%', '111%', '110%', '109%'],
        ['NRR — Mid-market',              '108%', '107%', '106%', '105%', '104%', '102%'],
    ]
)

add_insight(doc,
    'Read: Sales efficiency has declined every single quarter for two years. '
    'The magic number at 0.92 is a caution signal (below 1.0). Adding quota-carrying '
    'headcount is not the answer — productivity per rep must improve.')

add_body(doc,
    'These numbers tell me that the organization ran hard through a disorienting '
    'period — a CEO transition, an AI pivot, a segment reorg, an acquisition — and '
    'it is tired. My commitment, starting now, is to give this team a clear '
    'strategic direction and to hold it. No more pivots. The direction we set at '
    'Investor Day is the direction we execute against for three years.',
    space_after=8)

# ── What I Am Asking ──────────────────────────────────────────────────────────
add_section_heading(doc, 'What I Am Asking From This Board')

add_body(doc,
    'Three things, specifically.',
    space_after=4)

bullets = [
    ('1.  Alignment on the strategic framing.',
     'At Investor Day I will answer the question "what is Meridian" — project '
     'management tool with AI features, or agentic work platform with PM as one '
     'surface. The board needs to be aligned before that answer goes public. I am '
     'asking for that conversation today.'),
    ('2.  Guidance on the M&A question.',
     'We have two acquisition targets in early diligence. We have four hundred '
     'sixty-three million in cash and no debt. The board authorized a buyback; '
     'I believe the better use of capital in the next twelve months is targeted '
     'acquisition of AI capability. I would like the board\'s read on risk tolerance '
     'and deal size before I bring a specific recommendation.'),
    ('3.  Support on talent.',
     'I am requesting board approval to refresh senior engineering compensation '
     'in Q1. The People and Compensation Committee has the details. The risk of '
     'inaction — losing fifteen to twenty-five senior engineers in a market where '
     'AI talent is scarce — is more expensive than the cost of acting.'),
]

for heading, body_text in bullets:
    p, run = add_body(doc, heading, space_before=4, space_after=2, size=11)
    run.bold = True
    add_body(doc, body_text, space_before=0, space_after=8, size=11)

# ── Close ─────────────────────────────────────────────────────────────────────
add_rule(doc, 'C89A2A', 8)

add_body(doc,
    'The deceleration is real. The enterprise franchise is a genuine asset. '
    'The AI gap is closing. The organization needs a steady hand and a clear story. '
    'That is what I am here to provide.',
    space_before=10, space_after=6)

add_body(doc,
    'Let\'s get to work.',
    space_before=0, space_after=20)

p, run = add_body(doc, 'Catherine Park', space_before=0, space_after=2, size=11)
run.bold = True
add_body(doc, 'President & Chief Executive Officer, Meridian Technologies', size=10)
add_body(doc, 'May 2026', size=10)

# ── Save ──────────────────────────────────────────────────────────────────────
doc.save('/home/user/ddfd/meridian_board_opening_statement.docx')
print('Saved: meridian_board_opening_statement.docx')
