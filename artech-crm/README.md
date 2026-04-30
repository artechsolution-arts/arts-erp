# Artech CRM

A modern, open-source Customer Relationship Management system. Manage leads, deals, contacts, and communications in one place with a clean Vue.js-powered interface.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D?style=flat&logo=vuedotjs&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-4+-646CFF?style=flat&logo=vite&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat&logo=nodedotjs&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-10.6+-003545?style=flat&logo=mariadb&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-6+-DC382D?style=flat&logo=redis&logoColor=white)
![License](https://img.shields.io/badge/License-AGPLv3-blue?style=flat&logo=gnu&logoColor=white)

---

## Features

| Feature | Description |
|---------|-------------|
| 🎯 **Leads & Deals** | Full pipeline management with kanban and list views |
| 👤 **Contacts & Organizations** | Unified contact database with activity history |
| 📞 **Calls & Emails** | Integrated call logging and email communication |
| 🔀 **Assignment Rules** | Auto-assign leads/deals based on conditions |
| ⏱️ **SLA Management** | Service level agreement tracking on leads |
| 📧 **Email Templates** | Reusable templates for outreach |
| 🎛️ **Custom Fields & Views** | Fully customizable columns and filters |
| 📊 **Analytics & Reports** | Conversion rates, pipeline value, leaderboards |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white) | Backend API, webhooks, background jobs |
| ![Vue.js](https://img.shields.io/badge/-Vue.js_3-4FC08D?style=flat&logo=vuedotjs&logoColor=white) | Reactive SPA frontend |
| ![Vite](https://img.shields.io/badge/-Vite-646CFF?style=flat&logo=vite&logoColor=white) | Frontend build & dev server |
| ![TailwindCSS](https://img.shields.io/badge/-Tailwind_CSS-06B6D4?style=flat&logo=tailwindcss&logoColor=white) | Utility-first CSS framework |
| ![MariaDB](https://img.shields.io/badge/-MariaDB-003545?style=flat&logo=mariadb&logoColor=white) | Primary database |
| ![Redis](https://img.shields.io/badge/-Redis-DC382D?style=flat&logo=redis&logoColor=white) | Queue & real-time events |
| ![Twilio](https://img.shields.io/badge/-Twilio-F22F46?style=flat&logo=twilio&logoColor=white) | Voice calling integration |

---

## Requirements

| Dependency | Version |
|-----------|---------|
| ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white) | 3.10 or higher |
| ![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat&logo=nodedotjs&logoColor=white) | 18 or higher |
| ![MariaDB](https://img.shields.io/badge/MariaDB-10.6+-003545?style=flat&logo=mariadb&logoColor=white) | 10.6 or higher |
| ![Redis](https://img.shields.io/badge/Redis-6+-DC382D?style=flat&logo=redis&logoColor=white) | 6 or higher |
| ![Yarn](https://img.shields.io/badge/Yarn-1.22+-2C8EBB?style=flat&logo=yarn&logoColor=white) | 1.22 or higher |

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

The CRM frontend is a standalone ![Vue.js](https://img.shields.io/badge/-Vue.js_3-4FC08D?style=flat&logo=vuedotjs&logoColor=white) application built with ![Vite](https://img.shields.io/badge/-Vite-646CFF?style=flat&logo=vite&logoColor=white).

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

### ⚙️ CRM Settings

Navigate to **CRM > Settings > CRM Settings** to configure:
- Default lead assignment rules
- SLA policies
- Email integration
- Telephony integration (Twilio)

### 📧 Email Integration

Go to **Settings > Email Domain** and configure your SMTP/IMAP settings to enable:
- Sending emails from CRM
- Email-to-Lead conversion
- Auto-reply templates

### 📞 Twilio Integration (Calling)

![Twilio](https://img.shields.io/badge/Twilio-Voice_Integration-F22F46?style=flat&logo=twilio&logoColor=white)

In **CRM > Settings > CRM Settings**:
1. Enter your Twilio Account SID
2. Enter your Auth Token
3. Set your Twilio phone number
4. Enable call logging

### 🔀 Assignment Rules

Go to **CRM > Configuration > Assignment Rule** to create rules that automatically assign leads and deals based on:
- Round-robin rotation
- Lead source
- Geography / territory
- Custom conditions

---

## Access & Permissions

| Role | Permissions |
|------|-------------|
| 🔑 CRM Manager | Full access — all leads, deals, settings |
| 👤 CRM User | Own records + assigned records |
| 📈 Sales Manager | Read-all, assign, delete |
| 🚫 Guest | No access |

Assign roles via **Setup > User > Roles**.

---

## Key Workflows

### 🎯 Lead Lifecycle

```
New Lead → Contacted → Nurturing → Qualified → Converted (Deal) → Won / Lost
```

### 💼 Deal Pipeline

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

![License](https://img.shields.io/badge/License-AGPLv3-blue?style=flat&logo=gnu&logoColor=white)
AGPLv3 — see [LICENSE](LICENSE)

## Contact

![Gmail](https://img.shields.io/badge/Email-artechnical707%40gmail.com-D14836?style=flat&logo=gmail&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-artechsolution--arts-181717?style=flat&logo=github&logoColor=white)
