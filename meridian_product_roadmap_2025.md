# Meridian Product Roadmap — 2025 Year-End Status

*Internal — Chief Product Officer to CEO, January 2026.*

This document tracks 2025 roadmap commitments against actual delivery, plus
a brief look ahead to 2026.

## 2025 Commitments — Status

| Commitment | Original GA target | Actual GA | Slip | Status notes |
|------------|--------------------|-----------|------|--------------|
| AI Copilot — closed beta | Q4 2024 | Q4 2024 | 0 | On time. ~40 enterprise design partners. |
| AI Copilot — open beta | Q1 2025 | Q2 2025 | 1 quarter | Held to harden security and multi-tenant isolation. |
| AI Copilot — GA | Q2 2025 | Q3 2025 | 1 quarter | Released September 2025. |
| Microservices refactor (core PM) | Q4 2024 | Q3 2025 | 3 quarters | Significant scope expansion driven by Copilot dependencies. |
| FedRAMP Moderate certification | Q3 2024 | Q3 2024 | 0 | On time. |
| HIPAA / BAA support | Q1 2024 | Q1 2024 | 0 | On time. |
| GxP-validated environment | Q4 2025 | DEFERRED | n/a | Deferred to 2026. Insufficient demand from pharma pipeline to justify. |
| Mobile redesign | Q2 2025 | Q3 2025 | 1 quarter | Minor slip. NPS in mobile cohort up from 38 to 47 post-launch. |
| Native Slack integration v2 | Q3 2025 | Q4 2025 | 1 quarter | Slack API changes forced rework. |
| Resource management module | Q4 2025 | DEFERRED | n/a | Deprioritized in favor of agentic-experiences work. |
| Time tracking module | Q3 2025 | Q4 2025 | 1 quarter | Shipped, modest adoption. |
| Workflow automation v2 | Q2 2025 | Q4 2025 | 2 quarters | Reframed as "agentic workflows" mid-year, scope expanded. |
| Helio Labs integration (post-acquisition) | Q4 2025 (announced) | In progress | n/a | Half of Helio team integrated into Copilot product org. |

## Headline Themes from 2025

1. **AI moved to the center.** Roadmap items not related to AI/agentic
   features were systematically deprioritized through the year. This was
   the right call but it had collateral damage on mid-market expansion
   features (resource mgmt, time tracking) that customers were asking for.

2. **Slip rate of one quarter is the new normal.** Six of twelve
   commitments slipped one quarter; two slipped multiple quarters; two
   were deferred. Engineering attributes this primarily to (a) Copilot
   infrastructure being more complex than estimated and (b) the
   microservices refactor consuming more capacity than planned.

3. **Helio acquisition already paying off.** The Helio team has moved a
   key Copilot architectural decision (agent orchestration) from "needs
   six months of design work" to "we have a working pattern from day one."

## 2026 Roadmap — Working Draft (Not Yet Board-Approved)

| Commitment | Target GA | Strategic rationale |
|------------|-----------|---------------------|
| Copilot — Enterprise governance suite | Q1 2026 | Required to win regulated-industry deals; enterprise admins need full audit, role-based agent permissions, model selection. |
| Copilot — In-product agent builder | Q2 2026 | Customer-built agents as a differentiator vs. closed agent suites (Asana, Monday). |
| Resource management module (resurrected) | Q2 2026 | Mid-market expansion lever. Top-3 ask in customer advisory board. |
| Workflow marketplace | Q3 2026 | Network effects: customers share agents, drives stickiness and SMB self-serve resurgence. |
| Pricing model refresh | Q3 2026 | Move from per-seat to per-seat-plus-consumption for AI features. Required by economics of agentic usage. |
| GxP-validated environment | Q4 2026 | Pharma pipeline now warrants the investment; three named accounts. |

## Risks and Asks

- **Engineering capacity is the binding constraint.** We have 750 engineers.
  The 2026 plan assumes we hire 80 more in H1 (mostly AI-adjacent). At
  current attrition (~15% annual), net adds are closer to 25.
- **The Copilot pricing model is a strategic decision, not a product
  decision.** A consumption-based model implies a different sales motion
  and different revenue forecasting discipline. CPO recommends CFO and CRO
  jointly own this.
- **The agent-builder roadmap depends on Helio retention.** The Helio
  retention agreements run through 2028. If the team unwinds early — for
  example after their cash compensation cliff in 2026 — the roadmap is
  exposed.
