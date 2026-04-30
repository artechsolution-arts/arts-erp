# Artech ERP

The core ERP application — a complete business management system covering Accounting, Inventory, Sales, Purchasing, and Manufacturing.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-10.6+-003545?style=flat&logo=mariadb&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-6+-DC382D?style=flat&logo=redis&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat&logo=nodedotjs&logoColor=white)
![License](https://img.shields.io/badge/License-GPLv3-blue?style=flat&logo=gnu&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-supported-000000?style=flat&logo=apple&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-supported-FCC624?style=flat&logo=linux&logoColor=black)
![Windows](https://img.shields.io/badge/Windows_WSL2-supported-0078D6?style=flat&logo=windows&logoColor=white)

---

## Modules

| Module | Description |
|--------|-------------|
| 💰 **Accounts** | Chart of accounts, invoices, payments, tax, GST/VAT, budgets, financial reports |
| 📦 **Stock** | Warehouses, items, stock entries, serial/batch tracking, valuation |
| 🛒 **Selling** | Quotations, sales orders, delivery notes, pricing rules |
| 🏭 **Buying** | Purchase orders, supplier management, purchase receipts |
| ⚙️ **Manufacturing** | BOM, work orders, production planning |
| 📋 **Projects** | Project tracking, tasks, timesheets |
| 🤝 **CRM** | Leads, opportunities, communications |
| 🏗️ **Assets** | Asset management, depreciation |
| 🔧 **Maintenance** | Maintenance schedules and visits |
| 🎧 **Support** | Issues, warranty claims |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white) | Backend logic, REST API, background jobs |
| ![MariaDB](https://img.shields.io/badge/-MariaDB-003545?style=flat&logo=mariadb&logoColor=white) | Primary database |
| ![Redis](https://img.shields.io/badge/-Redis-DC382D?style=flat&logo=redis&logoColor=white) | Queue, cache, real-time pub/sub |
| ![Node.js](https://img.shields.io/badge/-Node.js-339933?style=flat&logo=nodedotjs&logoColor=white) | Frontend build toolchain |
| ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | Frontend scripting |
| ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat&logo=html5&logoColor=white) | Jinja2-based print formats & templates |
| ![Git](https://img.shields.io/badge/-Git-F05032?style=flat&logo=git&logoColor=white) | Version control |

---

## Requirements

| Dependency | Version |
|-----------|---------|
| ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white) | 3.10 or higher |
| ![MariaDB](https://img.shields.io/badge/MariaDB-10.6+-003545?style=flat&logo=mariadb&logoColor=white) | 10.6 or higher |
| ![Redis](https://img.shields.io/badge/Redis-6+-DC382D?style=flat&logo=redis&logoColor=white) | 6 or higher |
| ![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat&logo=nodedotjs&logoColor=white) | 18 or higher |
| ![Git](https://img.shields.io/badge/Git-2.x-F05032?style=flat&logo=git&logoColor=white) | 2.x |

---

## Installation

This app is installed as part of the Artech ERP Platform. See the [root setup guide](../README.md) for full instructions.

### Standalone Install

```bash
# From inside your bench directory
bench get-app artech https://github.com/artechsolution-arts/arts-erp
bench --site your-site.local install-app artech
```

### Post-Install Setup Wizard

After installing, open your browser and navigate to the site. The Setup Wizard will guide you through:

1. 🌍 **Language & Region** — Select your language, country, and timezone
2. 🏢 **Company** — Create your first company with currency and fiscal year
3. 📊 **Chart of Accounts** — Choose a standard chart (or import your own)
4. 🧾 **Tax Template** — Set up applicable tax rates
5. 📂 **Opening Balances** — Import opening stock and accounting balances

---

## Configuration

### 🏢 Company Setup

Go to **Setup > Company** and configure:
- Company name, abbreviation, country
- Default currency and fiscal year
- Tax IDs (GST/VAT/PAN)
- Company logo

### 💰 Accounting Settings

Go to **Accounts > Accounting Settings**:
- Enable perpetual inventory (recommended)
- Set default payment terms
- Configure automatic bank reconciliation

### 📦 Stock Settings

Go to **Stock > Stock Settings**:
- Enable serialized inventory if needed
- Set default valuation method (FIFO / Moving Average)
- Configure auto-reorder rules

### 🧾 Tax Setup

Navigate to **Accounts > Tax > Sales Taxes and Charges Template**:
- Create tax templates for your region
- Assign to items and customers/suppliers

---

## Key Workflows

### 🛒 Sales Cycle

```
Lead → Opportunity → Quotation → Sales Order → Delivery Note → Sales Invoice → Payment
```

### 🏭 Purchase Cycle

```
Material Request → Request for Quotation → Purchase Order → Purchase Receipt → Purchase Invoice → Payment
```

### ⚙️ Manufacturing Cycle

```
BOM → Production Plan → Work Order → Stock Entry (Manufacture) → Finished Goods
```

---

## Reports

| Category | Reports |
|----------|---------|
| 💰 **Accounts** | Profit & Loss, Balance Sheet, Trial Balance, General Ledger, AR/AP |
| 📦 **Stock** | Stock Balance, Stock Ledger, Stock Ageing, Valuation |
| 🛒 **Sales** | Sales Register, Item-wise Sales, Sales Analytics |
| 🏭 **Purchase** | Purchase Register, Item-wise Purchase, Purchase Analytics |

---

## Customization

### 🔧 Adding Custom Fields

Go to **Setup > Customize Form** and select any DocType to add custom fields without modifying code.

### 📝 Custom Scripts

Use **Setup > Client Script** or **Setup > Server Script** for custom business logic.

### 🖨️ Print Formats

Go to **Setup > Print Format** to create custom document templates with Jinja2 templating.

---

## Migrations & Patches

```bash
bench --site your-site.local migrate
```

---

## License

![License](https://img.shields.io/badge/License-GPLv3-blue?style=flat&logo=gnu&logoColor=white)
GNU General Public License v3.0

## Contact

![Gmail](https://img.shields.io/badge/Email-artechnical707%40gmail.com-D14836?style=flat&logo=gmail&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-artechsolution--arts-181717?style=flat&logo=github&logoColor=white)
