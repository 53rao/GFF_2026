# SBI Multi-Agent Proactive Banking Engagement System

A multi-agent AI system for proactive banking customer engagement, built with **Next.js 15 (App Router, TypeScript)**.

---

## Project Structure

```
/
├── frontend/
│   └── nextjs-app/                    ← Next.js 15 App (App Router, TypeScript)
│       ├── app/
│       │   ├── (user)/                ← User interface route group
│       │   │   ├── layout.tsx         ← Top navbar layout
│       │   │   ├── login/page.tsx     ← User login (visual only)
│       │   │   ├── dashboard/page.tsx ← Account overview
│       │   │   ├── transactions/      ← Transaction history
│       │   │   └── notifications/     ← Engagement messages
│       │   ├── (admin)/               ← Admin interface route group
│       │   │   ├── layout.tsx         ← Sidebar layout
│       │   │   ├── admin/login/       ← Admin login (visual only)
│       │   │   ├── admin/dashboard/   ← Ops overview dashboard
│       │   │   ├── admin/cases/       ← Case queue
│       │   │   ├── admin/agents/      ← Agent pipeline
│       │   │   └── admin/handoffs/    ← Handoff management
│       │   ├── globals.css            ← Imports all shared styles
│       │   └── layout.tsx             ← Root HTML shell
│       ├── components/
│       │   ├── user/UserNav.tsx       ← User top navigation bar
│       │   └── admin/AdminSidebar.tsx ← Admin sidebar
│       ├── lib/
│       │   └── mock-data.ts           ← All mock data (no API calls)
│       └── styles/
│           ├── tokens.css             ← CSS custom properties (design tokens)
│           ├── base.css               ← Reset + global typography
│           ├── user.css               ← User interface styles
│           └── admin.css              ← Admin interface styles
├── backend/
│   ├── agents/     ← Placeholder (not implemented)
│   ├── api/        ← Placeholder (not implemented)
│   ├── config/     ← Placeholder (not implemented)
│   └── db/         ← Placeholder (not implemented)
└── README.md
```

---

## Getting Started

```bash
cd frontend/nextjs-app
npm run dev
# App runs at http://localhost:3000
```

| URL | Page |
|---|---|
| `http://localhost:3000` | → Redirects to `/login` |
| `/login` | User login (visual only) |
| `/dashboard` | User account dashboard |
| `/transactions` | Transaction history |
| `/notifications` | Engagement notifications |
| `/admin/login` | Admin login (visual only) |
| `/admin/dashboard` | Operations overview |
| `/admin/cases` | Case queue |
| `/admin/agents` | Agent pipeline |
| `/admin/handoffs` | Handoff management |

---

## Tech Stack

| Category | Choice |
|---|---|
| Framework | Next.js 15 (App Router) |
| Language | TypeScript |
| Styling | Vanilla CSS + CSS Custom Properties |
| Data | Static mock data in `lib/mock-data.ts` |
| Fonts | Inter (Google Fonts) |

---

## Design System

Defined once in `styles/tokens.css`, consumed by both interfaces via `globals.css`.

| Token | Value | Usage |
|---|---|---|
| `--color-primary` | `hsl(210, 72%, 38%)` | SBI blue — nav, buttons |
| `--color-primary-pale` | `hsl(210, 60%, 95%)` | Card highlights, chips |
| `--color-bg` | `hsl(210, 30%, 97%)` | Page backgrounds |
| `--color-surface` | `#ffffff` | Cards, panels |
| `--font-sans` | `Inter, system-ui` | All text |
| `--radius-card` | `12px` | Card corners |
| `--shadow-card` | `0 2px 12px …` | Card elevation |

---

## Backend (Placeholder Only)

Backend folders exist as empty stubs — no logic implemented at this stage:
- `/backend/agents/` — Multi-agent orchestration (future)
- `/backend/api/` — REST/WebSocket endpoints (future)
- `/backend/config/` — Configuration (future)
- `/backend/db/` — Database layer (future)