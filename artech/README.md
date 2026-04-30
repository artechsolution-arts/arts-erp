# Artech ERP

The core ERP application — a complete business management system covering Accounting, Inventory, Sales, Purchasing, and Manufacturing.

---

## Modules

| Module | Description |
|--------|-------------|
| **Accounts** | Chart of accounts, invoices, payments, tax, GST/VAT, budgets, financial reports |
| **Stock** | Warehouses, items, stock entries, serial/batch tracking, valuation |
| **Selling** | Quotations, sales orders, delivery notes, pricing rules |
| **Buying** | Purchase orders, supplier management, purchase receipts |
| **Manufacturing** | BOM, work orders, production planning |
| **Projects** | Project tracking, tasks, timesheets |
| **CRM** | Leads, opportunities, communications |
| **Assets** | Asset management, depreciation |
| **Maintenance** | Maintenance schedules and visits |
| **Support** | Issues, warranty claims |

---

## Requirements

- Python 3.10+
- artech_engine (Artech Framework) — version 15+
- MariaDB 10.6+
- Redis 6+
- Node.js 18+

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

1. **Language & Region** — Select your language, country, and timezone
2. **Company** — Create your first company with currency and fiscal year
3. **Chart of Accounts** — Choose a standard chart (or import your own)
4. **Tax Template** — Set up applicable tax rates
5. **Opening Balances** — Import opening stock and accounting balances

---

## Configuration

### Company Setup

Go to **Setup > Company** and configure:
- Company name, abbreviation, country
- Default currency and fiscal year
- Tax IDs (GST/VAT/PAN)
- Company logo

### Accounting Settings

Go to **Accounts > Accounting Settings**:
- Enable perpetual inventory (recommended)
- Set default payment terms
- Configure automatic bank reconciliation

### Stock Settings

Go to **Stock > Stock Settings**:
- Enable serialized inventory if needed
- Set default valuation method (FIFO / Moving Average)
- Configure auto-reorder rules

### Tax Setup

Navigate to **Accounts > Tax > Sales Taxes and Charges Template**:
- Create tax templates for your region
- Assign to items and customers/suppliers

---

## Key Workflows

### Sales Cycle

```
Lead → Opportunity → Quotation → Sales Order → Delivery Note → Sales Invoice → Payment
```

### Purchase Cycle

```
Material Request → Request for Quotation → Purchase Order → Purchase Receipt → Purchase Invoice → Payment
```

### Manufacturing Cycle

```
BOM → Production Plan → Work Order → Stock Entry (Manufacture) → Finished Goods
```

---

## Reports

Key financial and operational reports available:

- **Accounts:** Profit & Loss, Balance Sheet, Trial Balance, General Ledger, Accounts Receivable/Payable
- **Stock:** Stock Balance, Stock Ledger, Stock Ageing, Valuation Reports
- **Sales:** Sales Register, Item-wise Sales, Sales Analytics
- **Purchase:** Purchase Register, Item-wise Purchase, Purchase Analytics

---

## Customization

### Adding Custom Fields

Go to **Setup > Customize Form** and select any DocType to add custom fields without modifying code.

### Custom Scripts

Use **Setup > Client Script** or **Setup > Server Script** for custom business logic.

### Print Formats

Go to **Setup > Print Format** to create custom document templates with Jinja2 templating.

---

## Migrations & Patches

Run pending database migrations:

```bash
bench --site your-site.local migrate
```

---

## License

GNU General Public License v3.0

## Contact

Email: artechnical707@gmail.com
GitHub: https://github.com/artechsolution-arts/arts-erp
