# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Strategic intelligence and board document generation for **Meridian Technologies (MRDN)**, a fictional ~$400M ARR project management SaaS company. The repo combines raw source data (CSVs, markdown) with Python generators that produce polished board-ready outputs (`.docx`, `.pdf`, `.png`).

## Running the generators

```bash
python generate_chart.py          # outputs meridian_board_chart.png
python generate_board_doc.py      # outputs meridian_board_opening_statement.docx
python generate_board_pdf.py      # outputs meridian_board_opening_statement.pdf
```

All three scripts are standalone — no arguments, no config files. They read hardcoded data inline (not from the CSVs) and write output files to the working directory.

Dependencies (no requirements.txt — install manually if missing):

```bash
pip install python-docx reportlab matplotlib numpy
```

## Architecture

The repository has two layers:

**Source data layer** (markdown + CSV files) — the authoritative record of Meridian's financials, strategy, customer feedback, competitive landscape, and internal memos. These are the inputs for any analysis or new document generation.

**Generator layer** (three Python scripts) — each script hard-codes the content and data it needs directly in the script body. They do not import from each other or read the CSV/markdown files at runtime. If you update the source data, you must also update the relevant generator script manually.

Key data files and what they contain:
- `meridian_financials_2022_2025.csv` — quarterly P&L and balance sheet metrics, Q1 2022–Q4 2025
- `meridian_kpis_2024.csv` — NRR, GRR, churn, CAC payback, magic number, AI Copilot seat ramp by quarter
- `meridian_financials_summary.csv` — point-in-time snapshot of liquidity, guidance, R&D budget, Helio acquisition cost

Key strategic files:
- `meridian_internal_brief.md` — CEO briefing framing the Option A vs. Option B positioning decision
- `meridian_ai_strategy_options.md` — full detail on both options (PM-with-AI vs. agentic platform), including hiring mix, pricing model, M&A pipeline, and 2028 revenue shape
- `meridian_recent_customer_feedback.md` — synthesized customer voice from Dec 2025–Feb 2026
- `competitors_cached/` — pre-extracted AI posture summaries for Asana, Monday, Smartsheet, Atlassian (use as fallback if live WebFetch of URLs in `competitors.md` returns 403)

## Generator internals

All three scripts share a consistent visual identity: navy (`#0D2B55`), slate (`#44546E`), gold (`#C89A2A`) palette, Calibri font in the docx/pdf scripts, DejaVu Sans in the chart script. When adding new sections, follow the existing helper function patterns (`add_section_heading`, `add_body`, `add_insight` in the doc script; `section`, `body`, `insight` in the pdf script; `axis_style`, `bar_label` in the chart script).

The chart script uses `matplotlib.use('Agg')` — no display needed, safe to run headless.

## Branch

Active development branch: `claude/setup-exercise-2-data-vY96z`
