# Artech ERP

Enterprise resource planning platform — Accounting, Buying, Selling, Inventory, Manufacturing, Projects, HR, and more.

![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)

---

## One-Command Setup

`setup.sh` installs **every dependency**, creates the database, creates the site, installs the app, and launches it. Nothing else needed.

### ![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)

```bash
git clone https://github.com/YOUR_ORG/artech.git
cd artech
bash setup.sh
```

### ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)

```bash
git clone https://github.com/YOUR_ORG/artech.git
cd artech
bash setup.sh
```

### ![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white) WSL 2

`setup.sh` detects Windows and prints WSL 2 instructions automatically.  
Open **PowerShell as Administrator** and run once:

```powershell
wsl --install
```

Restart, open **Ubuntu** from the Start Menu, then run:

```bash
git clone https://github.com/YOUR_ORG/artech.git
cd artech
bash setup.sh
```

---

## What Gets Installed Automatically

| Dependency | Version | ![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white) | ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black) | ![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white) WSL |
|---|---|---|---|---|
| Python | 3.13+ | Homebrew | apt / dnf | apt |
| Node.js | 18+ | Homebrew | NodeSource | NodeSource |
| MariaDB | 10.6+ | Homebrew | apt / dnf | apt |
| Redis | 6+ | Homebrew | apt / dnf | apt |
| wkhtmltopdf | 0.12+ | Homebrew | apt | apt |
| bench CLI | latest | pip | pip | pip |
| ngrok | 3+ | Homebrew | apt | apt |
| cloudflared | latest | Homebrew | wget | wget |

---

## Configuration

`setup.sh` creates a `.env` file automatically by asking you a few questions.  
You can also create it manually before running setup:

```bash
cp .env.example .env
# edit .env with your values
bash setup.sh
```

### `.env` reference

| Variable | Description | Default |
|---|---|---|
| `SITE_NAME` | Local site hostname | `artech.localhost` |
| `SITE_ADMIN_PASSWORD` | Admin login password | `admin` |
| `DB_NAME` | MariaDB database name | `artech_site` |
| `DB_USER` | MariaDB username | `artech_site` |
| `DB_PASSWORD` | MariaDB password | `artech123` |
| `PORT` | Local server port | `8000` |
| `NGROK_AUTHTOKEN` | ngrok auth token (for public URL) | — |
| `NGROK_STATIC_DOMAIN` | Permanent public domain | — |

> `.env` is **git-ignored** — your passwords and tokens never get committed.

---

## Permanent Public URL (Optional)

By default the app is accessible at `http://localhost:8000`.  
For a **permanent public URL** that never changes (share with clients, CEO, remote team):

1. Sign up free at **https://ngrok.com**
2. Copy your **Authtoken** from the ngrok dashboard
3. Claim your **free Static Domain** (`your-name.ngrok-free.app`)
4. Add both to `.env`:

```env
NGROK_AUTHTOKEN=your_authtoken_here
NGROK_STATIC_DOMAIN=your-name.ngrok-free.app
```

5. Run `./artech-start.sh` — the same URL works every time, from anywhere, on any device.

> Without ngrok, the script falls back to a temporary Cloudflare URL (changes on each restart).

---

## Daily Usage

You can run `artech-start.sh` from **either** the cloned repo folder **or** the bench folder — both work the same way.

### ![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)

```bash
# From the cloned repo
cd artech
./artech-start.sh

# Or from the bench
cd ~/artech-bench
./artech-start.sh
```

### ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)

```bash
cd artech
./artech-start.sh
# or
cd ~/artech-bench
./artech-start.sh
```

### ![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white) WSL 2

Open **Ubuntu** from the Start Menu, then:

```bash
cd artech
./artech-start.sh
# or
cd ~/artech-bench
./artech-start.sh
```

---

### Stop
```bash
./artech-start.sh stop
```

### Restart
```bash
./artech-start.sh restart
```

### Status
```bash
./artech-start.sh status
```

> **Note:** If you run `./artech-start.sh` before running `setup.sh`, you will see:
> ```
>   Bench not found at ~/artech-bench
>   Run setup first:  bash setup.sh
> ```

Sample output after a successful start:

```
  ✅  Artech ERP is LIVE!

  Login        :  Administrator / admin
  Local URL    :  http://localhost:8000
  Public URL   :  https://your-domain.ngrok-free.app  ← PERMANENT
```

---

## Login

| Field | Value |
|---|---|
| URL | `http://localhost:8000` or your ngrok domain |
| Username | `Administrator` |
| Password | `SITE_ADMIN_PASSWORD` from `.env` (default: `admin`) |

---

## Project Structure

```
artech/                    ← this repo (the app)
├── artech/                # Python app code
│   ├── accounts/          # Accounting module
│   ├── buying/            # Buying module
│   ├── selling/           # Selling module
│   ├── stock/             # Inventory module
│   ├── manufacturing/     # Manufacturing module
│   ├── projects/          # Projects module
│   └── ...
├── setup.sh               # ← One-command full setup
├── artech-start.sh        # ← Start / stop / status
├── .env.example           # ← Configuration template
├── .env                   # Your local config (git-ignored)
└── README.md              # This file
```

The bench that runs the app is created at `~/artech-bench/` during setup.

---

## Logs

```bash
tail -f ~/artech-bench/logs/web.log        # Web server
tail -f ~/artech-bench/logs/worker.log     # Background jobs
tail -f ~/artech-bench/logs/scheduler.log  # Scheduled tasks
```

---

## Updating

```bash
git pull origin main
cd ~/artech-bench
bench --site artech.localhost migrate
./artech-start.sh restart
```

---

## Troubleshooting

### MariaDB not starting

| | Command |
|---|---|
| ![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white) | `brew services start mariadb` |
| ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black) | `sudo systemctl start mariadb` |
| ![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white) WSL | `sudo service mysql start` |

Check status:
```bash
brew services list | grep mariadb       # macOS
sudo systemctl status mariadb           # Linux / WSL
```

### Redis not starting

| | Command |
|---|---|
| ![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white) | `brew services start redis` |
| ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black) | `sudo systemctl start redis-server` |
| ![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white) WSL | `sudo service redis-server start` |

### Port 8000 already in use

```bash
./artech-start.sh stop

# macOS / Linux / WSL
lsof -ti:8000 | xargs kill -9
```

### bench command not found

| | Command |
|---|---|
| ![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white) | `export PATH="/opt/homebrew/bin:/Library/Frameworks/Python.framework/Versions/3.13/bin:$PATH"` |
| ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black) / ![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white) WSL | `export PATH="$HOME/.local/bin:$PATH"` |

Then verify: `bench --version`

### Full reset (wipe site and start fresh)

```bash
./artech-start.sh stop
bench drop-site artech.localhost --force
bash setup.sh
```

---

## Support

| | |
|---|---|
| **Email** | support@artech.com |
| **Bugs** | bugs@artech.com |
| **Hours** | Mon – Fri · 9 AM – 6 PM IST |
