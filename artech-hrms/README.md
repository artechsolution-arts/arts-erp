# Artech HR

Modern HR and Payroll management built on top of Artech ERP. Handles the complete employee lifecycle from onboarding to payroll processing.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D?style=flat&logo=vuedotjs&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat&logo=nodedotjs&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-10.6+-003545?style=flat&logo=mariadb&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-6+-DC382D?style=flat&logo=redis&logoColor=white)
![License](https://img.shields.io/badge/License-GPLv3-blue?style=flat&logo=gnu&logoColor=white)
![Requires](https://img.shields.io/badge/Requires-Artech_ERP-orange?style=flat&logo=checkmarx&logoColor=white)

---

## Features

### 👥 Human Resources

| Feature | Description |
|---------|-------------|
| 🧑‍💼 **Employee Management** | Profiles, documents, org chart |
| 📅 **Leave Management** | Leave types, allocations, applications, holiday lists |
| ✅ **Attendance** | Manual, biometric import, shift management |
| 🔍 **Recruitment** | Job openings, applicants, offer letters |
| ⭐ **Appraisals** | Goal setting, 360-degree reviews, KPI tracking |
| 🧾 **Expense Claims** | Submit, approve, and reimburse employee expenses |

### 💵 Payroll

| Feature | Description |
|---------|-------------|
| 📊 **Salary Structures** | Configurable components (Basic, HRA, PF, ESI, TDS, etc.) |
| 🧾 **Salary Slips** | Auto-generation based on attendance and leaves |
| 🏢 **Payroll Entry** | Bulk salary processing by department/branch |
| 🏦 **Bank Disbursement** | Export salary payment files |
| 📋 **Tax Computation** | IT declarations, Form 16, TDS worksheets |
| 🇮🇳 **Statutory Compliance** | PF, ESI, PT, LWF |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white) | Backend logic, payroll computation, API |
| ![Vue.js](https://img.shields.io/badge/-Vue.js_3-4FC08D?style=flat&logo=vuedotjs&logoColor=white) | Employee self-service portal frontend |
| ![Vite](https://img.shields.io/badge/-Vite-646CFF?style=flat&logo=vite&logoColor=white) | Frontend build toolchain |
| ![TailwindCSS](https://img.shields.io/badge/-Tailwind_CSS-06B6D4?style=flat&logo=tailwindcss&logoColor=white) | Utility-first CSS |
| ![MariaDB](https://img.shields.io/badge/-MariaDB-003545?style=flat&logo=mariadb&logoColor=white) | Primary database |
| ![Redis](https://img.shields.io/badge/-Redis-DC382D?style=flat&logo=redis&logoColor=white) | Queue & background jobs |

---

## Requirements

| Dependency | Version |
|-----------|---------|
| ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white) | 3.10 or higher |
| ![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat&logo=nodedotjs&logoColor=white) | 18 or higher |
| ![MariaDB](https://img.shields.io/badge/MariaDB-10.6+-003545?style=flat&logo=mariadb&logoColor=white) | 10.6 or higher |
| ![Redis](https://img.shields.io/badge/Redis-6+-DC382D?style=flat&logo=redis&logoColor=white) | 6 or higher |
| ![Yarn](https://img.shields.io/badge/Yarn-1.22+-2C8EBB?style=flat&logo=yarn&logoColor=white) | 1.22 or higher |
| Artech ERP | 15+ (**required first**) |

> ⚠️ Artech HR requires the core **Artech ERP** app to be installed first.

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

### 👥 HR Settings

Go to **HR > Settings > HR Settings**:
- Set working hours
- Configure leave encashment policy
- Set retirement age
- Enable Employee Self Service

### 💵 Payroll Settings

Go to **Payroll > Settings > Payroll Settings**:
- Set payroll frequency (Monthly/Weekly)
- Configure currency and rounding
- Enable salary slip email dispatch
- Set payroll account heads

### 📅 Leave Policy Setup

1. Create **Leave Types** (Annual, Sick, Casual, Maternity, etc.)
2. Create a **Leave Policy** grouping leave types with annual limits
3. Assign policy to employees via **Leave Policy Assignment**
4. Run **Leave Allocation Tool** to allocate leaves for the period

### 📊 Salary Structure Setup

1. Go to **Payroll > Salary Component** and create earnings and deductions
2. Create a **Salary Structure** with components and their formulas
3. Assign via **Salary Structure Assignment** to employees
4. Verify with a test **Salary Slip**

---

## Payroll Processing Workflow

```
✅ 1. Mark Attendance (daily / upload)
              ↓
📅 2. Process Leave Applications
              ↓
🏢 3. Run Payroll Entry (select period + department)
              ↓
🧾 4. Review & Submit Salary Slips
              ↓
🏦 5. Create Bank Payment Entry
              ↓
📤 6. Export Bank Transfer File
```

---

## Statutory Compliance (India) 🇮🇳

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

### 📋 Manual Attendance
Upload via **HR > Attendance > Upload Attendance** using the CSV template.

### 🔐 Biometric Integration
Use the **Attendance Device** doctype to map punches from biometric machines.

### 🕐 Shift Management
1. Create **Shift Types** with timing and grace periods
2. Assign shifts to employees
3. Auto-generate attendance from shift logs

---

## Key Reports

| Report | Module |
|--------|--------|
| 💰 Monthly Salary Register | Payroll |
| 📅 Employee Leave Balance | HR |
| ✅ Attendance Sheet | HR |
| 👥 Employee Head Count | HR |
| 🔍 Recruitment Analytics | HR |
| 🏦 Bank Disbursement | Payroll |

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

![License](https://img.shields.io/badge/License-GPLv3-blue?style=flat&logo=gnu&logoColor=white)
GNU General Public License v3.0 — see [license.txt](license.txt)

## Contact

![Gmail](https://img.shields.io/badge/Email-artechnical707%40gmail.com-D14836?style=flat&logo=gmail&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-artechsolution--arts-181717?style=flat&logo=github&logoColor=white)
