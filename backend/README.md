# SBI Multi-Agent Proactive Banking Engagement Backend

FastAPI and LangGraph powered backend scaffolding for autonomous, multi-agent banking engagement and compliance orchestration.

## Architecture Overview

The system runs a stateful LangGraph workflow where agents collaborate over shared customer context:
1. **SentinelAgent**: Monitors transaction streams and app telemetry for opportunities or risk signals.
2. **MemoryAgent**: Retrieves customer 360 profile, channel preferences, and longitudinal history.
3. **AnalystAgent**: Investigates signals and formulates ranked engagement hypotheses grounded in RAG docs.
4. **PolicyAgent**: Strictly enforces RBI, TRAI, DPDP Act 2023, and internal business rules.
5. **EngagementStrategyAgent**: Schedules personalized outreach across Voice/SMS/Email channels.
6. **CallerAgent**: Executes real-time outbound Twilio voice interactions using LLM dialogue steering.
7. **TranscriptAnalyzerAgent**: Classifies engagement outcomes and intent commitments.
8. **RouterAgent**: Handles escalations to specialized human branch teams.

## Directory Structure

```
backend/
├── app/
│   ├── main.py               # FastAPI entrypoint & router registration
│   ├── config.py             # Pydantic BaseSettings environment configuration
│   ├── agents/               # Individual agent classes inheriting from BaseAgent
│   ├── graph/                # LangGraph StateGraph, nodes, and conditional edges
│   ├── api/                  # REST endpoints (cases, agents, admin, user, webhooks)
│   ├── db/                   # Async SQLAlchemy models, sessions, and CRUD stubs
│   ├── memory/               # Vector store wrapper & customer memory schemas
│   ├── rag/                  # Document ingestion & retrieval stubs
│   ├── voice/                # Twilio, STT, and TTS integrations
│   ├── data_simulation/      # Synthetic transaction & behavior generators
│   └── policies/             # Regulatory guardrail rules and notes
├── tests/                    # Unit & integration test stubs
├── requirements.txt
└── .env.example
```

## Running Verification

To verify import safety without external DB dependencies:
```bash
cd backend
python3 -c "import app.main; print('Import verification passed!')"
```
