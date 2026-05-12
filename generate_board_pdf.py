from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY   = colors.HexColor('#0D2B55')
SLATE  = colors.HexColor('#44546E')
GOLD   = colors.HexColor('#C89A2A')
LIGHT  = colors.HexColor('#F0F4F8')
WHITE  = colors.white
INK    = colors.HexColor('#1A1A2E')

# ── Document ──────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    '/home/user/ddfd/meridian_board_opening_statement.pdf',
    pagesize=LETTER,
    leftMargin=1.15*inch, rightMargin=1.15*inch,
    topMargin=1.0*inch,   bottomMargin=1.0*inch,
)

# ── Styles ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle = S('Title',
    fontName='Helvetica-Bold', fontSize=22, textColor=NAVY,
    spaceAfter=4, leading=26)

sSubtitle = S('Subtitle',
    fontName='Helvetica', fontSize=12, textColor=SLATE,
    spaceAfter=4, leading=16)

sMeta = S('Meta',
    fontName='Helvetica', fontSize=9.5, textColor=SLATE,
    spaceAfter=14, leading=13)

sSection = S('Section',
    fontName='Helvetica-Bold', fontSize=7.5, textColor=NAVY,
    spaceBefore=14, spaceAfter=3, leading=10,
    letterSpacing=0.8)

sBody = S('Body',
    fontName='Helvetica', fontSize=10.5, textColor=INK,
    spaceAfter=6, leading=15, wordWrap='LTR')

sBodyBold = S('BodyBold',
    fontName='Helvetica-Bold', fontSize=10.5, textColor=INK,
    spaceAfter=2, leading=15, spaceBefore=6)

sInsight = S('Insight',
    fontName='Helvetica-Oblique', fontSize=9, textColor=SLATE,
    spaceAfter=10, spaceBefore=4, leading=13,
    leftIndent=12, borderPadding=(0,0,0,8))

sClose = S('Close',
    fontName='Helvetica', fontSize=10.5, textColor=INK,
    spaceAfter=6, leading=15, spaceBefore=10)

sSig = S('Sig',
    fontName='Helvetica-Bold', fontSize=10.5, textColor=INK,
    spaceAfter=2, spaceBefore=18, leading=14)

sSigSub = S('SigSub',
    fontName='Helvetica', fontSize=9.5, textColor=SLATE,
    spaceAfter=2, leading=13)

sTableHdr = S('TableHdr',
    fontName='Helvetica-Bold', fontSize=8, textColor=WHITE,
    alignment=TA_CENTER, leading=10)

sTableCell = S('TableCell',
    fontName='Helvetica', fontSize=8, textColor=INK,
    alignment=TA_CENTER, leading=11)

sTableCellL = S('TableCellL',
    fontName='Helvetica', fontSize=8, textColor=INK,
    alignment=TA_LEFT, leading=11)

# ── Table builder ─────────────────────────────────────────────────────────────
def make_table(headers, rows, col_widths):
    data = [[Paragraph(h, sTableHdr) for h in headers]]
    for r_idx, row in enumerate(rows):
        cells = []
        for c_idx, val in enumerate(row):
            style = sTableCellL if c_idx == 0 else sTableCell
            cells.append(Paragraph(val, style))
        data.append(cells)

    total = sum(col_widths)
    scaled = [w / total * 6.2 * inch for w in col_widths]

    alt_rows = []
    for i in range(len(rows)):
        if i % 2 == 0:
            alt_rows.append(('BACKGROUND', (0, i+1), (-1, i+1), LIGHT))

    style = TableStyle([
        ('BACKGROUND',  (0,0), (-1,0), NAVY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT, WHITE]),
        ('GRID',        (0,0), (-1,-1), 0.25, colors.HexColor('#C8D0DA')),
        ('TOPPADDING',  (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING',(0,0), (-1,-1), 5),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
    ])

    t = Table(data, colWidths=scaled)
    t.setStyle(style)
    return t

def insight(text):
    return Paragraph(text, sInsight)

def gold_rule():
    return HRFlowable(width='100%', thickness=1.5, color=GOLD, spaceAfter=10, spaceBefore=10)

def navy_rule():
    return HRFlowable(width='100%', thickness=1, color=NAVY, spaceAfter=10, spaceBefore=2)

def section(text):
    return Paragraph(text.upper(), sSection)

def body(text):
    return Paragraph(text, sBody)

def sp(h=6):
    return Spacer(1, h)

# ── Build story ───────────────────────────────────────────────────────────────
story = []

# Cover
story += [
    Paragraph('MERIDIAN TECHNOLOGIES', sTitle),
    Paragraph('Annual Board Strategic Review', sSubtitle),
    Paragraph('CEO Opening Statement  ·  May 2026  ·  ~5 minutes', sMeta),
    navy_rule(),
    sp(4),
]

# Opening
story += [
    section('Opening'),
    body('Thank you. Before we move into the prepared agenda, I want to take five '
         'minutes to give you my honest read on where this company stands — not the '
         'investor-relations version, but the CEO version.'),
    body('I have been in this role for fifteen months. I have spent time with our '
         'largest customers, our board, and every layer of this organization. What I '
         'want to share today is what I have concluded, what concerns me, and what I '
         'am asking from you.'),
    sp(4),
]

# Where We Stand
story += [
    section('Where We Stand'),
    body('The headline numbers are solid. Full-year 2025 revenue of four hundred '
         'million dollars, up eleven percent. Operating margin of twelve percent, up '
         'from five percent three years ago. Four hundred sixty-three million in cash '
         'and no debt. Free cash flow margin approaching eighteen percent.'),
    body('Those numbers deserve acknowledgment. Lenore built a financially disciplined '
         'business, and this team has continued that discipline through a transition '
         'year. I am proud of it.'),
    body('And I want to be equally honest about what those numbers conceal. Revenue '
         'growth has decelerated every single year — twenty-eight percent in 2022, '
         'sixteen in 2024, eleven in 2025, and we are guiding ten to fourteen for 2026. '
         'That is not a coincidence. That is a structural pattern, and it is the central '
         'issue this board needs to help me address.'),
    sp(6),
]

# Exhibit 1
story += [
    KeepTogether([
        section('Exhibit 1 — Company Financials: Full-Year Snapshot'),
        sp(3),
        make_table(
            headers=['Metric', 'FY 2022', 'FY 2023', 'FY 2024', 'FY 2025', '2026 Guide'],
            col_widths=[2.1, 0.82, 0.82, 0.82, 0.82, 0.9],
            rows=[
                ['Revenue ($M)',       '$260',  '$311',  '$360',  '$400',  '$440–455'],
                ['YoY Revenue Growth', '—',     '+19%',  '+16%',  '+11%',  '+10–14%'],
                ['ARR ($M)',           '$275',  '$328',  '$375',  '$413',  '—'],
                ['Gross Margin',       '78.0%', '78.6%', '79.2%', '79.6%', '—'],
                ['Operating Margin',   '5.1%',  '7.7%',  '10.0%', '12.4%', '14–15%'],
                ['FCF Margin',         '10.4%', '13.9%', '16.2%', '17.8%', '—'],
                ['Cash ($M)',          '$344',  '$392',  '$432',  '$463',  '—'],
            ]
        ),
        sp(4),
        insight('Read: Revenue growth decelerates every year as margins expand. The business is more '
                'profitable and slower-growing simultaneously — a pattern that demands a deliberate '
                'strategic answer in 2026.'),
    ]),
]

# Issue 1
story += [
    section('Issue 1 — Growth Deceleration'),
    body('The first issue is growth deceleration, and the segment picture explains it '
         'precisely. We are not one company — we are three businesses in one P&L, and '
         'they are moving in very different directions.'),
    sp(4),
    KeepTogether([
        section('Exhibit 2 — Segment ARR: Three-Year Mix Shift'),
        sp(3),
        make_table(
            headers=['Segment', 'ARR Q4\'22', 'Mix', 'ARR Q4\'25', 'Mix', 'YoY', 'NRR', 'Churn'],
            col_widths=[1.05, 0.88, 0.48, 0.88, 0.48, 0.6, 0.6, 0.63],
            rows=[
                ['Enterprise', '~$74M',  '27%', '~$167M', '40%', '+21%', '125%', '2.6%'],
                ['Mid-market', '~$96M',  '35%', '~$194M', '47%', '+6%',  '102%', '10.2%'],
                ['SMB',        '~$105M', '38%', '~$52M',  '13%', '–23%', '84%',  '22.1%'],
                ['Total',      '~$275M', '100%','~$413M', '100%', '+10%','109%', '—'],
            ]
        ),
        sp(4),
        insight('Read: Enterprise has nearly doubled its ARR share (27% → 40%) and is the engine of '
                'the business. SMB has collapsed (38% → 13%) and is an active drag. Mid-market, at '
                '47% of ARR, is the swing segment — and at 6% growth with NRR of 102%, it is barely '
                'treading water.'),
    ]),
    body('The SMB decline costs us approximately thirty million dollars of growth '
         'headwind in 2026 alone. I have made the decision to run SMB on a '
         'self-funded basis. The segment will stand on its own economics or we will '
         'manage it down in a controlled way. We will not subsidize it from enterprise '
         'margins.'),
    sp(6),
]

# Issue 2
story += [
    section('Issue 2 — AI Competitive Position'),
    body('The second issue is AI. I will not soften this: we were late. Asana shipped '
         'their agent in the fall of 2024. We shipped AI Copilot to general '
         'availability in September 2025. Asana has since bundled AI into their '
         'standard tier. Monday is now larger than us by ARR. ClearAI Work raised '
         'a hundred-and-twenty-million-dollar round at a billion-dollar valuation and '
         'is taking our SMB.'),
    body('And yet — the early Copilot numbers give me genuine confidence that we can '
         'compete. Seven hundred ten paying seats at year-end, against an internal '
         'target of six hundred. A forty-four-percent attach rate on enterprise renewals '
         'in Q4, against a target of forty percent. The Helio Labs acquisition — '
         'twenty-eight engineers from leading AI labs, a working agent framework — '
         'compressed our roadmap by an estimated fifteen months.'),
    sp(4),
    KeepTogether([
        section('Exhibit 3 — AI Copilot Ramp'),
        sp(3),
        make_table(
            headers=['Quarter', 'Paying Seats', 'ARR Contribution', 'Enterprise Attach Rate'],
            col_widths=[1.55, 1.1, 1.45, 2.1],
            rows=[
                ['Q4 2024 (closed beta)', '0',   '$0',      '—'],
                ['Q1 2025',               '0',   '$0',      '—'],
                ['Q2 2025 (open beta)',   '140', '~$0.7M',  '—'],
                ['Q3 2025 (GA Sep)',      '420', '~$2.0M',  '—'],
                ['Q4 2025',               '710', '~$3.5M',  '44%  ✓  (target: 40%)'],
            ]
        ),
        sp(4),
        insight('Read: Copilot is early-stage at $3.5M ARR, but the Q4 attach rate of 44% is the '
                'most important leading indicator in this business. If it holds as the enterprise '
                'renewal base cycles through 2026, AI becomes a material growth driver — not a cost.'),
    ]),
    body('I will share the full AI roadmap at Investor Day on March eleventh. What I '
         'will say here is that our enterprise differentiation — FedRAMP Moderate, '
         'HIPAA, the governance and audit features that regulated industries require — '
         'is where we win, and where Asana does not. We will build our AI strategy '
         'around that moat.'),
    sp(6),
]

# Issue 3
story += [
    section('Issue 3 — Organizational Readiness'),
    body('The third issue is internal, and the one I am most focused on. The October '
         'employee survey — eighty-one percent response rate — was candid. '
         'Thirty-one percent of engineering open-ends cited roadmap thrash as their '
         'primary frustration. Nineteen percent of all employees said they cannot '
         'clearly articulate what makes Meridian different from Asana with AI. '
         'Twenty-seven percent of senior engineers said their compensation is not '
         'keeping pace with the market.'),
    sp(4),
    KeepTogether([
        section('Exhibit 4 — Sales Efficiency Trend'),
        sp(3),
        make_table(
            headers=['Metric', 'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q4 2025'],
            col_widths=[1.9, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75],
            rows=[
                ['Magic Number',            '1.20',   '1.16',   '1.10',   '1.05',   '1.02',   '0.92'],
                ['CAC Payback (months)',     '18.2',   '18.9',   '19.5',   '20.4',   '21.1',   '22.4'],
                ['New ARR / Rep ($K)',       '$1,320', '$1,290', '$1,255', '$1,210', '$1,180', '$1,110'],
                ['NRR — Overall',           '114%',   '113%',   '112%',   '111%',   '110%',   '109%'],
                ['NRR — Mid-market',        '108%',   '107%',   '106%',   '105%',   '104%',   '102%'],
            ]
        ),
        sp(4),
        insight('Read: Sales efficiency has declined every single quarter for two years. The magic '
                'number at 0.92 is a caution signal (below 1.0). Adding quota-carrying headcount '
                'is not the answer — productivity per rep must improve.'),
    ]),
    body('These numbers tell me that the organization ran hard through a disorienting '
         'period — a CEO transition, an AI pivot, a segment reorg, an acquisition — and '
         'it is tired. My commitment, starting now, is to give this team a clear '
         'strategic direction and to hold it. No more pivots. The direction we set at '
         'Investor Day is the direction we execute against for three years.'),
    sp(6),
]

# What I Am Asking
story += [
    section('What I Am Asking From This Board'),
    body('Three things, specifically.'),
    sp(4),
    Paragraph('<b>1.  Alignment on the strategic framing.</b>', sBody),
    body('At Investor Day I will answer the question "what is Meridian" — project '
         'management tool with AI features, or agentic work platform with PM as one '
         'surface. The board needs to be aligned before that answer goes public. I am '
         'asking for that conversation today.'),
    sp(4),
    Paragraph('<b>2.  Guidance on the M&amp;A question.</b>', sBody),
    body('We have two acquisition targets in early diligence. We have four hundred '
         'sixty-three million in cash and no debt. The board authorized a buyback; '
         'I believe the better use of capital in the next twelve months is targeted '
         'acquisition of AI capability. I would like the board\'s read on risk '
         'tolerance and deal size before I bring a specific recommendation.'),
    sp(4),
    Paragraph('<b>3.  Support on talent.</b>', sBody),
    body('I am requesting board approval to refresh senior engineering compensation '
         'in Q1. The People and Compensation Committee has the details. The risk of '
         'inaction — losing fifteen to twenty-five senior engineers in a market where '
         'AI talent is scarce — is more expensive than the cost of acting.'),
    sp(8),
]

# Close
story += [
    gold_rule(),
    Paragraph('The deceleration is real. The enterprise franchise is a genuine asset. '
              'The AI gap is closing. The organization needs a steady hand and a clear story. '
              'That is what I am here to provide.', sClose),
    Paragraph('Let\'s get to work.', sClose),
    sp(10),
    Paragraph('Catherine Park', sSig),
    Paragraph('President &amp; Chief Executive Officer, Meridian Technologies', sSigSub),
    Paragraph('May 2026', sSigSub),
]

doc.build(story)
print('Saved: meridian_board_opening_statement.pdf')
