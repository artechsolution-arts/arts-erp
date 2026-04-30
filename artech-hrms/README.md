# Artech HR

Modern HR and Payroll management built on top of Artech ERP. Handles the complete employee lifecycle from onboarding to payroll processing.

---

## Features

### Human Resources
- **Employee Management** — Profiles, documents, org chart
- **Leave Management** — Leave types, allocations, applications, holiday lists
- **Attendance** — Manual, biometric import, shift management
- **Recruitment** — Job openings, applicants, offer letters
- **Appraisals** — Goal setting, 360-degree reviews, KPI tracking
- **Expense Claims** — Submit, approve, and reimburse employee expenses

### Payroll
- **Salary Structures** — Configurable components (Basic, HRA, PF, ESI, TDS, etc.)
- **Salary Slips** — Auto-generation based on attendance and leaves
- **Payroll Entry** — Bulk salary processing by department/branch
- **Bank Disbursement** — Export salary payment files
- **Tax Computation** — IT declarations, Form 16, TDS worksheets
- **Statutory Compliance** — PF, ESI, PT, LWF

---

## Requirements

- Python 3.10+
- Node.js 18+ and yarn
- artech_engine (Artech Framework) — version 15+
- artech (Artech ERP) — version 15+ (**required**)
- MariaDB 10.6+
- Redis 6+

> Artech HR requires the core Artech ERP app to be installed first.

---

## Installation

### Step 1 — Install Artech ERP First

```bash
bench get-app artech https://github.com/artechsolution-arts/arts-erp
bench --site your-site.local install-app artech
```

### Step 2 — Install Artech HR

```bash
bench get-app artech_hrms https://github.com/artechsolution-arts/arts-erp
bench --site your-site.local install-app artech_hrms
```

### Verify Installation

```bash
bench --site your-site.local list-apps
# Should show both: artech, artech_hrms
```

---

## Frontend Development Setup

```bash
cd artech-hrms/frontend
yarn install
yarn dev
```

Make sure your bench is running (`bench start`) in a separate terminal.

### Build for Production

```bash
yarn build
```

---

## Configuration

### HR Settings

Go to **HR > Settings > HR Settings**:
- Set working hours
- Configure leave encashment policy
- Set retirement age
- Enable Employee Self Service

### Payroll Settings

Go to **Payroll > Settings > Payroll Settings**:
- Set payroll frequency (Monthly/Weekly)
- Configure currency and rounding
- Enable salary slip email dispatch
- Set payroll account heads

### Leave Policy Setup

1. Create **Leave Types** (Annual, Sick, Casual, Maternity, etc.)
2. Create a **Leave Policy** grouping leave types with annual limits
3. Assign policy to employees via **Leave Policy Assignment**
4. Run **Leave Allocation Tool** to allocate leaves for the period

### Salary Structure Setup

1. Go to **Payroll > Salary Component** and create earnings and deductions
2. Create a **Salary Structure** with components and their formulas
3. Assign via **Salary Structure Assignment** to employees
4. Verify with a test **Salary Slip**

---

## Payroll Processing Workflow

```
1. Mark Attendance (daily / upload)
        ↓
2. Process Leave Applications
        ↓
3. Run Payroll Entry (select period + department)
        ↓
4. Review & Submit Salary Slips
        ↓
5. Create Bank Payment Entry
        ↓
6. Export Bank Transfer File
```

---

## Statutory Compliance (India)

### Provident Fund (PF)
- Configure PF account in **Salary Component**
- Set employee and employer contribution rates
- Generate ECR file for EPFO portal

### ESI
- Enable ESI in **Salary Component**
- System auto-calculates based on gross salary threshold
- Generate ESI challan report

### TDS / Income Tax
- Employees submit IT declarations
- System computes monthly TDS deduction
- Generate Form 16 at year end

---

## Attendance Integration

### Manual Attendance
Upload via **HR > Attendance > Upload Attendance** using the CSV template.

### Biometric Integration
Use the **Attendance Device** doctype to map punches from biometric machines.

### Shift Management
1. Create **Shift Types** with timing and grace periods
2. Assign shifts to employees
3. Auto-generate attendance from shift logs

---

## Key Reports

| Report | Location |
|--------|----------|
| Monthly Salary Register | Payroll > Reports |
| Employee Leave Balance | HR > Reports |
| Attendance Sheet | HR > Reports |
| Employee Head Count | HR > Reports |
| Recruitment Analytics | HR > Reports |
| Bank Disbursement | Payroll > Reports |

---

## Running Tests

```bash
bench --site your-site.local run-tests --app artech_hrms
```

---

## Upgrading

```bash
cd artech-bench
bench update --apps artech_hrms
bench --site your-site.local migrate
```

---

## License

GNU General Public License v3.0 — see [license.txt](license.txt)

## Contact

Email: artechnical707@gmail.com
GitHub: https://github.com/artechsolution-arts/arts-erp
