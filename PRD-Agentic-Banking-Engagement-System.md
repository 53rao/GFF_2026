# PRD: Agentic AI Proactive Customer Engagement System
### Theme: Agentic AI & Emerging Tech — Track 3

---

## 1. Overview

**Problem Statement (Track 3):**
"Create AI-driven engagement models that proactively interact with customers based on behaviours, financial patterns, and life events."

**One-line summary:**
A multi-agent system that autonomously detects meaningful changes in a customer's financial and behavioral patterns, reasons about *why* the change matters (life event, opportunity, or attrition risk), and decides — on its own — whether, when, how, and through which channel to engage the customer, across **payments, investments, insurance, and mobile banking adoption**.

**Why this matters:**
Banks today are either reactive (customer has to seek out products) or blast generic mass campaigns (low relevance, high cost, customer fatigue). This system replaces both with a governed, autonomous, per-customer engagement decision — reasoning through evidence rather than following static rules, and improving over time via memory of past interactions.

---

## 2. Goals

- Detect meaningful signals from transaction and behavioral data streams
- Reason over signals to form evidence-backed hypotheses (not rule lookups)
- Respect business/regulatory policy constraints before any customer-facing action
- Choose the right channel, timing, and objective per customer
- Execute engagement, evaluate the outcome, and route qualified leads to the right human team
- Learn from every interaction so future decisions for that customer improve
- Remain compliant with DPDP, TRAI, SEBI, and RBI-style constraints by design, not as an afterthought

**Non-goals (for this phase):**
- Not a general-purpose chatbot
- Not attempting full production-scale, real bank data integration
- Not implementing live Twilio voice calls at this stage (simulated transcripts are the interim substitute)

---

## 3. System Architecture — Agent Pipeline

The system is a 9-agent pipeline orchestrated via **LangGraph**, where each agent has exactly one responsibility and state flows through a shared `PipelineState` object.

```
Memory Read → Sentinel → Analyst → Policy Gate → Engagement Strategy
   → Caller → Transcript Analyzer → Memory Write / Router
```

| # | Agent | Responsibility |
|---|-------|-----------------|
| 1 | **Sentinel** (Detection) | Monitors transaction + behavioral streams; flags anomalies/signals. Lightweight, rule/statistical-based — no LLM. Scalable equivalent to real-time fraud detection architecture. |
| 2 | **Analyst** (Hypothesis) | Investigates flagged signals, correlates multiple weak signals over time into a ranked hypothesis. Tags each hypothesis to a product line: **payments, investments, insurance, or mobile banking adoption** — or to a **retention/attrition risk** category. LLM-driven, structured JSON output. |
| 3 | **Policy Agent** | Interprets current business/regulatory rules (fraud thresholds, VIP-always-human-review, RBI/SEBI/TRAI/DPDP constraints). Tells Coordinator what actions are permissible. Rule-matching logic against structured policy definitions. |
| 4 | **Engagement Strategy Agent** | Decides *when*, how often, with what objective (educate/convert/retain), and through which channel (call, WhatsApp, email, branch escalation) to engage — informed by Memory Agent's history. |
| 5 | **Memory Agent** | Maintains persistent, evolving history per customer — preferred channel, best contact windows, past response patterns. Read at pipeline start, written at pipeline end, so every future engagement is smarter. |
| 6 | **Coordinator** (Orchestrator) | Owns pipeline state per case. Decides next step, retries, skips, or halts. Gates every transition against Policy Agent's permission check. Implemented as the compiled LangGraph. |
| 7 | **Caller** (Voice/Engagement Execution) | Executes the engagement — adaptive, hypothesis-grounded conversation. Simulated transcript generation in this phase; designed to swap in live Twilio later without interface changes. |
| 8 | **Transcript Analyzer** (Lead-Rating) | Reads the engagement transcript, classifies outcome: hot lead / retention risk / not interested / follow-up needed, with reasoning. |
| 9 | **Router** (Handoff) | Forwards qualified cases to the correct human team/queue (Investment RM, Insurance desk, Retention team, Payments ops) based on Analyzer's classification and Analyst's product-line tag. |

**Key architectural principle:** cheap, high-throughput detection (Sentinel) filters millions of events down to a small number of flagged signals before any expensive LLM reasoning or human-facing action occurs — the same cost funnel pattern used in real-time fraud detection systems today.

---

## 4. Data Layer (Current Phase: JSON, Demo-Ready)

**Decision:** Using flat JSON files instead of a database for the demo phase — team is remote, git-diffable JSON is easier to collaborate on than a binary DB file, and the schema is designed to map 1:1 onto a future PostgreSQL migration.

**Entities (mirrors eventual SQL schema):**
- `customers.json` — profile, tier, tenure, product holdings
- `transactions.json` — transaction history, linked via `customer_id`
- `behavior_events.json` — app/login/navigation events, linked via `customer_id`
- `policy_rules.json` — structured condition/action business rules
- `signals.json` — Sentinel's output (generated at runtime)
- `hypotheses.json` — Analyst's output (generated at runtime)
- `engagement_cases.json`, `call_transcripts.json`, `engagement_outcomes.json` — pipeline execution records
- `customer_memory.json` — Memory Agent's evolving per-customer state

**Access pattern:** All reads/writes go through a single `data_store.py` module — no other file touches the JSON files directly. This means migrating to PostgreSQL later only requires rewriting the internals of `data_store.py`; every agent's calling code stays unchanged.

**Seed data design:** ~30 synthetic "boring" customers (Faker-generated, unremarkable data) + 4-5 hand-scripted customers with deliberate event timelines (e.g., salary increase → new recurring debit → app usage shift) so Sentinel's detection can be demonstrated against realistic signal-in-noise conditions, not random data.

---

## 5. Tech Stack

| Layer | Choice |
|---|---|
| Agent orchestration | LangGraph |
| LLM | Claude / GPT-4 (function-calling / structured JSON output) |
| Backend framework | FastAPI |
| Data store (current) | JSON files via `data_store.py` abstraction |
| Data store (future) | PostgreSQL (same schema shape) |
| Voice (future) | Twilio Voice + Whisper/Deepgram (STT) + ElevenLabs/Twilio (TTS) |
| RAG (future) | Product catalog + policy grounding for Caller's dialogue and Analyst's product matching |
| Frontend | React, two separate interfaces (see below) |
| Frontend icon library | lucide-react |

---

## 6. Frontend — Two Interfaces

**Design language:** SBI (State Bank of India) net-banking–inspired aesthetic — light blue and white palette, clean and trustworthy, conservative banking UI conventions.

### User-Facing Interface
- Customer-facing dashboard/portal (not a chatbot) — account overview, notifications/engagements received, transaction view
- Reflects what the customer sees when the system proactively reaches out

### Admin-Facing Interface
- Internal operations tool for the bank team
- Case queues, pipeline status per case, agent reasoning trace, handoff management
- Denser, table-heavy, functional layout — same color system as user interface for visual consistency, but styled as an enterprise tool

Both interfaces share a common design token system (`/frontend/shared`) for color, typography, and spacing consistency.

---

## 7. Compliance & Governance (Built-In, Not Bolted On)

- **DPDP Act (2023):** Consent layer controls what data categories drive inference; opt-out enforced upstream of Sentinel.
- **TRAI:** Policy Agent enforces consent-based outreach and blocks any channel the customer hasn't consented to for commercial contact.
- **SEBI:** Investment-related hypotheses are flagged for mandatory human RM review before outreach — no autonomous execution on investment advice, respecting suitability/disclosure norms.
- **RBI-style regulation:** Policy Agent structure allows immediate rule updates (e.g., freeze conditions) without re-architecting the pipeline.
- **Audit trail:** Every policy check is logged (`policy_checks`), making every autonomous decision traceable after the fact — a baseline requirement for any bank compliance review.

---

## 8. Business Model / Commercial Potential

**Monetization:**
- **Primary — per-activation licensing:** bank pays per successfully routed, human-verified qualified lead handed off through Router. Aligns cost directly with delivered value; low upfront adoption risk.
- **Secondary — tiered SaaS:** modular licensing (e.g., detection-only via Sentinel+Analyst vs. full stack including Caller/voice) enabling phased adoption.

**Value drivers:**
- Lower cost-per-conversion via confidence-matched, cost-tiered channel routing (expensive channels reserved for high-confidence/high-value cases)
- Reduced customer fatigue/attrition via Memory-informed contact frequency and channel matching
- Retention treated as a first-class detection category, not an afterthought
- Compliance-agile architecture — policy changes don't require pipeline re-engineering

---

## 9. Demo Scope & Build Priority

**Tier 1 (must-have for initial demo):**
1. Sentinel — real rule-based detection against seeded JSON data
2. Analyst — real LLM reasoning producing structured, ranked hypotheses
3. Coordinator (minimal LangGraph wiring) — proves real multi-agent orchestration, not sequential function calls

**Tier 2 (strong additions if time allows):**
4. Engagement Strategy Agent — channel/timing/objective decision logic
5. Transcript Analyzer — LLM classification of a simulated (not live-call) transcript

**Tier 3 (build if time remains):**
6. Caller — simulated transcript generation (live Twilio deferred)
7. Router — simple classification-to-queue mapping

**Described but not fully built for initial demo (mention verbally / mockup only):**
8. Policy Agent — shown as static rules JSON + a described gate in Coordinator's flow
9. Memory Agent — described as a roadmap capability with a mockup screen showing the "system adapts over time" narrative, since demonstrating it live requires multiple historical runs

**Core demo proof point:** Sentinel detecting a real, non-hardcoded anomaly in seeded data, Analyst reasoning over it with visible evidence-based logic, and the full trace rendered on the admin interface — this is what proves "agentic reasoning," not a rules engine with an LLM skin.

---

## 10. Explicit Non-Negotiables for Implementation

- No hardcoded/fake data returned from any API endpoint — unimplemented agents return HTTP 501, never mocked success responses
- Every agent output must be structured (JSON schema-validated), not free-text parsed
- Every agent's reasoning must be traceable end-to-end for the admin interface's case detail view
- Sentinel is intentionally rule/statistical-based, not LLM-based — this is a deliberate scalability decision, not a shortcut, and should be stated as such
