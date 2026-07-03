# Regulatory & Compliance Guardrails Reference

This document serves as reference for PolicyAgent verification logic and prompt engineering grounding.

## 1. TRAI (Telecom Regulatory Authority of India) Regulations
- **Calling Hours**: Outbound telemarketing/engagement calls are strictly restricted between **09:00 IST and 21:00 IST**.
- **DND Registry**: Customers registered on National Do Not Call (NDNC) registry must not be contacted via promotional voice or SMS channels unless explicit transaction/service exemption exists.

## 2. RBI (Reserve Bank of India) Guidelines
- **Contact Frequency**: Banks must avoid customer harassment. Proactive promotional or cross-sell outreach is capped at 4 attempts per calendar month.
- **Cooling-Off Period**: If a customer declines an offer or requests a pause, a mandatory 48-hour cooling-off period must elapse before any further outreach.

## 3. DPDP Act 2023 (Digital Personal Data Protection Act)
- **Explicit Consent**: Data utilization for proactive AI engagement requires explicit, affirmative customer consent tied to specific purpose codes.
- **Right to Erasure/Opt-Out**: Customers exercising opt-out rights must be immediately flagged in MemoryAgent and suppressed across all orchestration flows.

## 4. SEBI Guidelines (Investment Products)
- Any engagement involving mutual funds, securities, or wealth management must include mandatory risk disclosures without performance guarantees.
