# Artech CRM

A modern, open-source Customer Relationship Management system. Manage leads, deals, contacts, and communications in one place with a clean Vue.js-powered interface.

---

## Features

- **Leads & Deals** — Full pipeline management with kanban and list views
- **Contacts & Organizations** — Unified contact database with activity history
- **Calls & Emails** — Integrated call logging and email communication
- **Assignment Rules** — Auto-assign leads/deals based on conditions
- **SLA Management** — Service level agreement tracking on leads
- **Email Templates** — Reusable templates for outreach
- **Custom Fields & Views** — Fully customizable columns and filters
- **Analytics & Reports** — Conversion rates, pipeline value, leaderboards

---

## Requirements

- Python 3.10+
- Node.js 18+ and yarn
- artech_engine (Artech Framework) — version 15+
- MariaDB 10.6+
- Redis 6+

---

## Installation

### Via Bench

```bash
cd artech-bench

bench get-app artech_crm https://github.com/artechsolution-arts/arts-erp
bench --site your-site.local install-app artech_crm
```

### Verify Installation

```bash
bench --site your-site.local list-apps
```

---

## Frontend Development Setup

The CRM frontend is a standalone Vue.js application.

### Install Dependencies

```bash
cd artech-crm/frontend
yarn install
```

### Start Dev Server

```bash
yarn dev
```

Make sure your bench is running (`bench start`) before starting the frontend dev server.

### Build for Production

```bash
yarn build
```

Built assets are output to `artech_crm/public/frontend/`.

---

## Configuration

### CRM Settings

Navigate to **CRM > Settings > CRM Settings** to configure:
- Default lead assignment rules
- SLA policies
- Email integration
- Telephony integration (Twilio)

### Email Integration

Go to **Settings > Email Domain** and configure your SMTP/IMAP settings to enable:
- Sending emails from CRM
- Email-to-Lead conversion
- Auto-reply templates

### Twilio Integration (Calling)

In **CRM > Settings > CRM Settings**:
1. Enter your Twilio Account SID
2. Enter your Auth Token
3. Set your Twilio phone number
4. Enable call logging

### Assignment Rules

Go to **CRM > Configuration > Assignment Rule** to create rules that automatically assign leads and deals based on:
- Round-robin rotation
- Lead source
- Geography / territory
- Custom conditions

---

## Access & Permissions

| Role | Permissions |
|------|-------------|
| CRM Manager | Full access — all leads, deals, settings |
| CRM User | Own records + assigned records |
| Sales Manager | Read-all, assign, delete |
| Guest | No access |

Assign roles via **Setup > User > Roles**.

---

## Key Workflows

### Lead Lifecycle

```
New Lead → Contacted → Nurturing → Qualified → Converted (Deal) → Won / Lost
```

### Deal Pipeline

```
Prospecting → Qualification → Proposal → Negotiation → Closed Won / Closed Lost
```

---

## Running Tests

```bash
bench --site your-site.local run-tests --app artech_crm
```

---

## Upgrading

```bash
cd artech-bench
bench update --apps artech_crm
bench --site your-site.local migrate
```

---

## License

AGPLv3 — see [LICENSE](LICENSE)

## Contact

Email: artechnical707@gmail.com
GitHub: https://github.com/artechsolution-arts/arts-erp
