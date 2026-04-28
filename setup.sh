#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Artech ERP — One-Command Setup
#  Supports: macOS · Ubuntu/Debian · CentOS/RHEL/Fedora
#
#  Usage:
#    bash setup.sh
#
#  What it does:
#    1. Installs all system dependencies
#    2. Creates bench at ~/artech-bench
#    3. Installs Frappe framework
#    4. Links THIS repo as the artech app
#    5. Creates site, installs app
#    6. Launches everything
# ═══════════════════════════════════════════════════════════════

set -uo pipefail

# ── Colours ─────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${BLUE}  ▸${RESET} $*"; }
success() { echo -e "${GREEN}  ✔${RESET} $*"; }
warn()    { echo -e "${YELLOW}  ⚠${RESET}  $*"; }
error()   { echo -e "${RED}  ✖${RESET} $*" >&2; exit 1; }
step()    { echo -e "\n${BOLD}${CYAN}── $* ${RESET}"; }
ask()     { echo -ne "${YELLOW}  ?${RESET}  $1 "; }

# ── Detect OS ────────────────────────────────────────────────
OS="unknown"
ARCH="$(uname -m)"
PKG_MGR=""

if [[ "$(uname)" == "Darwin" ]]; then
    OS="mac"
elif [[ -f /etc/os-release ]]; then
    # shellcheck disable=SC1091
    source /etc/os-release
    case "${ID:-}" in
        ubuntu|debian|linuxmint|pop)        OS="debian"; PKG_MGR="apt" ;;
        centos|rhel|fedora|rocky|almalinux) OS="redhat"; PKG_MGR="dnf" ;;
        *) OS="linux-other" ;;
    esac
elif [[ "$(uname -s)" == MINGW* ]] || [[ "$(uname -s)" == CYGWIN* ]]; then
    OS="windows"
fi

# ── Windows: print WSL instructions and exit ─────────────────
if [[ "$OS" == "windows" ]]; then
    echo ""
    echo -e "${YELLOW}  Windows detected.${RESET}"
    echo -e "  Please use ${BOLD}WSL 2${RESET} (Windows Subsystem for Linux):"
    echo ""
    echo -e "  1. Open PowerShell as Administrator and run:"
    echo -e "     ${CYAN}wsl --install${RESET}"
    echo -e "  2. Restart your PC, then open Ubuntu from the Start Menu"
    echo -e "  3. Run this setup script again inside Ubuntu (WSL)"
    echo ""
    exit 0
fi

echo ""
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}${CYAN}   🚀  Artech ERP — Setup  ($OS / $ARCH)           ${RESET}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════${RESET}"

# ── Paths ────────────────────────────────────────────────────
# APP_DIR = this cloned repo (where setup.sh lives)
# BENCH_DIR = the bench that will be created at ~/artech-bench
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BENCH_DIR="$HOME/artech-bench"
ENV_FILE="$APP_DIR/.env"

# ── Load .env if it already exists ──────────────────────────
load_env() {
    [[ -f "$ENV_FILE" ]] || return
    while IFS='=' read -r key value; do
        [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
        value="${value%%#*}"
        value="${value%"${value##*[![:space:]]}"}"
        export "$key=$value"
    done < "$ENV_FILE"
}
load_env

# ── Defaults ─────────────────────────────────────────────────
FRAPPE_BRANCH="${FRAPPE_BRANCH:-version-15}"
SITE_NAME="${SITE_NAME:-artech.localhost}"
SITE_ADMIN_PASSWORD="${SITE_ADMIN_PASSWORD:-admin}"
DB_NAME="${DB_NAME:-artech_site}"
DB_USER="${DB_USER:-artech_site}"
DB_PASSWORD="${DB_PASSWORD:-artech123}"
PORT="${PORT:-8000}"
NGROK_AUTHTOKEN="${NGROK_AUTHTOKEN:-}"
NGROK_STATIC_DOMAIN="${NGROK_STATIC_DOMAIN:-}"

# ── Collect config interactively (first run only) ────────────
if [[ ! -f "$ENV_FILE" ]]; then
    echo ""
    echo -e "${BOLD}  Configuration  ${YELLOW}(press Enter to accept defaults)${RESET}"
    echo ""

    ask "Site admin password [$SITE_ADMIN_PASSWORD]:"
    read -r _input; [[ -n "$_input" ]] && SITE_ADMIN_PASSWORD="$_input"

    ask "Database password [$DB_PASSWORD]:"
    read -r _input; [[ -n "$_input" ]] && DB_PASSWORD="$_input"

    echo ""
    echo -e "  ${BOLD}Permanent Public URL  ${YELLOW}(optional)${RESET}"
    echo -e "  ${YELLOW}  Sign up FREE at https://ngrok.com for a static domain.${RESET}"
    ask "ngrok authtoken (or Enter to skip):"
    read -r NGROK_AUTHTOKEN
    if [[ -n "$NGROK_AUTHTOKEN" ]]; then
        ask "ngrok static domain (e.g. your-name.ngrok-free.app):"
        read -r NGROK_STATIC_DOMAIN
    fi

    cat > "$ENV_FILE" <<EOF
FRAPPE_BRANCH=$FRAPPE_BRANCH
SITE_NAME=$SITE_NAME
SITE_ADMIN_PASSWORD=$SITE_ADMIN_PASSWORD
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
PORT=$PORT
NGROK_AUTHTOKEN=$NGROK_AUTHTOKEN
NGROK_STATIC_DOMAIN=$NGROK_STATIC_DOMAIN
EOF
    success "Configuration saved to .env"
fi

# ═══════════════════════════════════════════════════════════════
step "1 / 7  System Packages"
# ═══════════════════════════════════════════════════════════════

if [[ "$OS" == "mac" ]]; then
    if ! command -v brew &>/dev/null; then
        info "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        [[ "$ARCH" == "arm64" ]] && eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
    success "Homebrew ready"

    info "Installing packages..."
    brew install python@3.13 node@18 mariadb redis git wkhtmltopdf 2>/dev/null || true
    brew link --force python@3.13 node@18 2>/dev/null || true
    export PATH="$(brew --prefix python@3.13)/bin:$(brew --prefix node@18)/bin:$PATH"

    brew install ngrok/ngrok/ngrok cloudflared 2>/dev/null || true

elif [[ "$OS" == "debian" ]]; then
    sudo apt-get update -qq
    sudo apt-get install -y -qq \
        python3 python3-pip python3-venv python3-dev \
        mariadb-server mariadb-client \
        redis-server \
        git curl wget \
        wkhtmltopdf \
        libssl-dev libffi-dev gcc g++ make \
        ca-certificates gnupg lsb-release

    # Node 18 via NodeSource
    if ! node --version 2>/dev/null | grep -qE "v18|v20"; then
        info "Installing Node.js 18..."
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt-get install -y nodejs
    fi

    # ngrok
    if ! command -v ngrok &>/dev/null; then
        info "Installing ngrok..."
        curl -fsSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
            | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
        echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
            | sudo tee /etc/apt/sources.list.d/ngrok.list >/dev/null
        sudo apt-get update -qq && sudo apt-get install -y ngrok 2>/dev/null || true
    fi

    # cloudflared
    if ! command -v cloudflared &>/dev/null; then
        CFARCH="amd64"; [[ "$ARCH" == "aarch64" ]] && CFARCH="arm64"
        wget -qO /tmp/cloudflared.deb \
            "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${CFARCH}.deb"
        sudo dpkg -i /tmp/cloudflared.deb 2>/dev/null || true
    fi

elif [[ "$OS" == "redhat" ]]; then
    sudo dnf install -y python3 python3-pip python3-devel \
        mariadb-server mariadb \
        redis git curl wget \
        openssl-devel libffi-devel gcc gcc-c++ make 2>/dev/null || \
    sudo yum install -y python3 python3-pip mariadb-server mariadb redis git 2>/dev/null || true

    if ! node --version 2>/dev/null | grep -qE "v18|v20"; then
        curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
        sudo dnf install -y nodejs 2>/dev/null || sudo yum install -y nodejs 2>/dev/null || true
    fi

    if ! command -v cloudflared &>/dev/null; then
        CFARCH="amd64"; [[ "$ARCH" == "aarch64" ]] && CFARCH="arm64"
        sudo wget -qO /usr/local/bin/cloudflared \
            "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${CFARCH}"
        sudo chmod +x /usr/local/bin/cloudflared
    fi
fi

success "System packages ready"

# ═══════════════════════════════════════════════════════════════
step "2 / 7  frappe-bench CLI"
# ═══════════════════════════════════════════════════════════════
if command -v bench &>/dev/null; then
    success "bench CLI already installed"
else
    info "Installing frappe-bench..."
    pip3 install frappe-bench 2>/dev/null || pip install frappe-bench
    success "bench CLI installed"
fi
export PATH="$HOME/.local/bin:/Library/Frameworks/Python.framework/Versions/3.13/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
BENCH_BIN="$(command -v bench)"

# ═══════════════════════════════════════════════════════════════
step "3 / 7  MariaDB"
# ═══════════════════════════════════════════════════════════════
start_mariadb() {
    if [[ "$OS" == "mac" ]]; then
        brew services start mariadb 2>/dev/null || true
    elif command -v systemctl &>/dev/null; then
        sudo systemctl enable mariadb --now 2>/dev/null || \
        sudo systemctl enable mysql --now 2>/dev/null || true
    else
        sudo service mysql start 2>/dev/null || true
    fi
}

if mysqladmin ping -uroot --silent 2>/dev/null; then
    success "MariaDB is running"
else
    info "Starting MariaDB..."
    start_mariadb; sleep 4
    mysqladmin ping -uroot --silent 2>/dev/null || error "MariaDB failed to start. Run: brew services start mariadb"
    success "MariaDB started"
fi

# Linux: configure charset for Frappe
if [[ "$OS" != "mac" ]]; then
    MYCNF="/etc/mysql/mariadb.conf.d/50-server.cnf"
    [[ -f "$MYCNF" ]] || MYCNF="/etc/mysql/my.cnf"
    if ! grep -q "innodb_file_per_table" "$MYCNF" 2>/dev/null; then
        info "Configuring MariaDB character set..."
        sudo tee -a "$MYCNF" >/dev/null <<MYCNF_EOF

[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
innodb_file_format = Barracuda
innodb_file_per_table = 1
innodb_large_prefix = 1
MYCNF_EOF
        start_mariadb; sleep 2
    fi
fi

# Create DB user
mysql -uroot 2>/dev/null <<MYSQL || mysql -uroot -p"$DB_PASSWORD" 2>/dev/null <<MYSQL || true
CREATE DATABASE IF NOT EXISTS \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'localhost';
GRANT ALL PRIVILEGES ON \`test_%\`.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
MYSQL
success "Database user ready"

# ═══════════════════════════════════════════════════════════════
step "4 / 7  Redis"
# ═══════════════════════════════════════════════════════════════
if redis-cli ping &>/dev/null; then
    success "Redis is running"
else
    info "Starting Redis..."
    if [[ "$OS" == "mac" ]]; then
        brew services start redis 2>/dev/null || true
    elif command -v systemctl &>/dev/null; then
        sudo systemctl enable redis-server --now 2>/dev/null || \
        sudo systemctl enable redis --now 2>/dev/null || true
    fi
    sleep 2
    redis-cli ping &>/dev/null && success "Redis started" || warn "Redis may need manual start"
fi

# ═══════════════════════════════════════════════════════════════
step "5 / 7  Bench + Frappe"
# ═══════════════════════════════════════════════════════════════
if [[ -d "$BENCH_DIR/apps/frappe" ]]; then
    success "Bench already exists at $BENCH_DIR"
else
    info "Creating bench at $BENCH_DIR (takes a few minutes)..."
    cd "$HOME"
    "$BENCH_BIN" init artech-bench \
        --frappe-branch "$FRAPPE_BRANCH" \
        --python "$(command -v python3)" \
        --verbose 2>&1 | grep -E "Getting|Installing|Cloning|Success|Error|WARNING" || true
    success "Bench created"
fi

cd "$BENCH_DIR"

# ── Link this repo as the artech app ─────────────────────────
if [[ -d "$BENCH_DIR/apps/artech" ]]; then
    success "artech app already present"
else
    info "Linking artech app from $APP_DIR ..."
    # Use bench get-app with local path — no re-download needed
    "$BENCH_BIN" get-app artech "$APP_DIR" || {
        # Fallback: copy directly
        info "Fallback: copying app directory..."
        cp -r "$APP_DIR" "$BENCH_DIR/apps/artech"
        cd "$BENCH_DIR"
        "$BENCH_BIN" pip install -e apps/artech 2>/dev/null || true
    }
    success "artech app linked"
fi

# ── Copy start script to bench root ──────────────────────────
cp "$APP_DIR/artech-start.sh" "$BENCH_DIR/artech-start.sh"
chmod +x "$BENCH_DIR/artech-start.sh"

# Copy .env to bench root (artech-start.sh reads it from there)
cp "$ENV_FILE" "$BENCH_DIR/.env"

# ═══════════════════════════════════════════════════════════════
step "6 / 7  Site"
# ═══════════════════════════════════════════════════════════════
cd "$BENCH_DIR"
SITE_DIR="$BENCH_DIR/sites/$SITE_NAME"

if [[ -d "$SITE_DIR" ]]; then
    success "Site $SITE_NAME already exists"
else
    info "Creating site $SITE_NAME (1-2 min)..."
    "$BENCH_BIN" new-site "$SITE_NAME" \
        --db-name "$DB_NAME" \
        --db-user "$DB_USER" \
        --db-password "$DB_PASSWORD" \
        --admin-password "$SITE_ADMIN_PASSWORD" \
        --no-mariadb-socket 2>&1 | tail -5
    "$BENCH_BIN" --site "$SITE_NAME" set-config developer_mode 1
    success "Site created"
fi

# Install artech on site
if ! "$BENCH_BIN" --site "$SITE_NAME" list-apps 2>/dev/null | grep -q artech; then
    info "Installing artech on site..."
    "$BENCH_BIN" --site "$SITE_NAME" install-app artech
    success "artech installed"
fi

echo "$SITE_NAME" > "$BENCH_DIR/sites/currentsite.txt"

# ═══════════════════════════════════════════════════════════════
step "7 / 7  ngrok (permanent URL)"
# ═══════════════════════════════════════════════════════════════
if [[ -n "$NGROK_AUTHTOKEN" ]] && command -v ngrok &>/dev/null; then
    ngrok config add-authtoken "$NGROK_AUTHTOKEN" 2>/dev/null && success "ngrok authtoken saved"
    [[ -n "$NGROK_STATIC_DOMAIN" ]] && \
        success "Permanent URL configured: https://$NGROK_STATIC_DOMAIN"
else
    warn "ngrok not configured — will use temporary Cloudflare URL on each start"
    info "For a permanent URL: add NGROK_AUTHTOKEN + NGROK_STATIC_DOMAIN to .env"
fi

# ── Done ─────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}  ✅  Setup complete! Artech ERP is ready.${RESET}"
echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════${RESET}"
echo ""
echo -e "  ${BOLD}Login:${RESET}   Administrator  /  $SITE_ADMIN_PASSWORD"
echo ""
echo -e "  ${BOLD}To start:${RESET}  ${CYAN}cd $BENCH_DIR && ./artech-start.sh${RESET}"
echo -e "  ${BOLD}To stop: ${RESET}  ${CYAN}./artech-start.sh stop${RESET}"
echo ""
[[ -n "$NGROK_STATIC_DOMAIN" ]] && \
    echo -e "  ${BOLD}Permanent URL:${RESET}  ${CYAN}${BOLD}https://$NGROK_STATIC_DOMAIN${RESET}"
echo ""

ask "Start Artech ERP now? [Y/n]:"
read -r _START_NOW
if [[ "${_START_NOW:-Y}" =~ ^[Yy]$ ]] || [[ -z "${_START_NOW:-}" ]]; then
    bash "$BENCH_DIR/artech-start.sh"
fi
