#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Artech ERP — Start / Stop
#
#  Start:   ./artech-start.sh
#  Stop:    ./artech-start.sh stop
#  Status:  ./artech-start.sh status
# ═══════════════════════════════════════════════════════════════

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── If run from the app repo, forward to the bench ───────────
# The bench lives at ~/artech-bench; this file ships inside the
# app repo. If apps/frappe doesn't exist here, we're in the repo.
if [[ ! -d "$SCRIPT_DIR/apps/frappe" ]]; then
    BENCH_TARGET="$HOME/artech-bench"
    if [[ -f "$BENCH_TARGET/artech-start.sh" ]]; then
        exec bash "$BENCH_TARGET/artech-start.sh" "${@}"
    else
        echo ""
        echo "  Bench not found at $BENCH_TARGET"
        echo "  Run setup first:  bash setup.sh"
        echo ""
        exit 1
    fi
fi

BENCH_DIR="$SCRIPT_DIR"
ENV_FILE="$BENCH_DIR/.env"
LOG_DIR="$BENCH_DIR/logs"
PID_DIR="$BENCH_DIR/.artech-pids"
TUNNEL_URL_FILE="$BENCH_DIR/.tunnel-url"

# ── Load .env ────────────────────────────────────────────────
if [[ -f "$ENV_FILE" ]]; then
    while IFS='=' read -r key value; do
        # Skip comments and blank lines
        [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
        # Strip inline comments and whitespace
        value="${value%%#*}"
        value="${value%"${value##*[![:space:]]}"}"
        export "$key=$value"
    done < "$ENV_FILE"
fi

# ── Defaults ─────────────────────────────────────────────────
SITE_NAME="${SITE_NAME:-artech.localhost}"
PORT="${PORT:-8000}"
DB_NAME="${DB_NAME:-artech_site}"
DB_USER="${DB_USER:-artech_site}"
DB_PASSWORD="${DB_PASSWORD:-artech123}"
NGROK_AUTHTOKEN="${NGROK_AUTHTOKEN:-}"
NGROK_STATIC_DOMAIN="${NGROK_STATIC_DOMAIN:-}"

BENCH_BIN="$(command -v bench 2>/dev/null || echo /Library/Frameworks/Python.framework/Versions/3.13/bin/bench)"
export PATH="/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.13/bin:$PATH"

# ── Colours ──────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${BLUE}  ▸${RESET} $*"; }
success() { echo -e "${GREEN}  ✔${RESET} $*"; }
warn()    { echo -e "${YELLOW}  ⚠${RESET}  $*"; }
error()   { echo -e "${RED}  ✖${RESET} $*" >&2; }

save_pid() { echo "$1" > "$PID_DIR/$2.pid"; }

# ── STATUS ───────────────────────────────────────────────────
show_status() {
    echo -e "\n${BOLD}  Artech ERP — Status${RESET}\n"
    local all_ok=true
    for svc in web worker scheduler cloudflare; do
        local pidfile="$PID_DIR/$svc.pid"
        if [[ -f "$pidfile" ]]; then
            local pid; pid=$(cat "$pidfile")
            if kill -0 "$pid" 2>/dev/null; then
                success "$svc  (PID $pid)"
            else
                error "$svc  (PID $pid — NOT running)"
                all_ok=false
            fi
        else
            warn "$svc  (not started)"
            all_ok=false
        fi
    done

    if [[ -f "$TUNNEL_URL_FILE" ]]; then
        echo ""
        echo -e "  ${BOLD}Public URL:${RESET}  ${CYAN}$(cat "$TUNNEL_URL_FILE")${RESET}"
    fi
    echo ""
    $all_ok && return 0 || return 1
}

# ── STOP ─────────────────────────────────────────────────────
stop_all() {
    echo -e "\n${BOLD}${RED}  Stopping Artech ERP...${RESET}\n"
    for pidfile in "$PID_DIR"/*.pid; do
        [[ -f "$pidfile" ]] || continue
        local pid; pid=$(cat "$pidfile")
        local name; name=$(basename "$pidfile" .pid)
        if kill "$pid" 2>/dev/null; then
            success "Stopped $name (PID $pid)"
        fi
        rm -f "$pidfile"
    done
    pkill -f "frappe serve --port $PORT" 2>/dev/null || true
    pkill -f "frappe worker"             2>/dev/null || true
    pkill -f "frappe schedule"           2>/dev/null || true
    pkill -f "cloudflared tunnel"        2>/dev/null || true
    pkill -f "ngrok http"                2>/dev/null || true
    rm -f "$TUNNEL_URL_FILE"
    echo ""
    success "All services stopped."
}

case "${1:-start}" in
    stop)   stop_all; exit 0 ;;
    status) show_status; exit $? ;;
    restart) stop_all; sleep 2 ;;
esac

# ── START ─────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}${CYAN}     🚀  Artech ERP — Starting Up                 ${RESET}"
echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════${RESET}"
echo ""

mkdir -p "$LOG_DIR" "$PID_DIR"
cd "$BENCH_DIR"

# ── 1. MariaDB ───────────────────────────────────────────────
info "Checking MariaDB..."
if mysql -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "SELECT 1;" &>/dev/null; then
    success "MariaDB is running"
else
    warn "MariaDB not responding — trying to start..."
    brew services start mariadb 2>/dev/null || mysql.server start 2>/dev/null || true
    sleep 3
    if mysql -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "SELECT 1;" &>/dev/null; then
        success "MariaDB started"
    else
        error "MariaDB failed. Run: brew services start mariadb"
        exit 1
    fi
fi

# ── 2. Redis cache ────────────────────────────────────────────
info "Checking Redis cache..."
if redis-cli -p 13000 ping &>/dev/null; then
    success "Redis cache running"
else
    redis-server "$BENCH_DIR/config/redis_cache.conf" --daemonize yes \
        --logfile "$LOG_DIR/redis_cache.log" 2>/dev/null
    sleep 1
    redis-cli -p 13000 ping &>/dev/null && success "Redis cache started" \
        || { error "Redis cache failed"; exit 1; }
fi

# ── 3. Redis queue ────────────────────────────────────────────
REDIS_Q_PORT=$(grep -E '^port' "$BENCH_DIR/config/redis_queue.conf" 2>/dev/null | awk '{print $2}' || echo "11000")
info "Checking Redis queue (port $REDIS_Q_PORT)..."
if redis-cli -p "$REDIS_Q_PORT" ping &>/dev/null; then
    success "Redis queue running"
else
    redis-server "$BENCH_DIR/config/redis_queue.conf" --daemonize yes \
        --logfile "$LOG_DIR/redis_queue.log" 2>/dev/null
    sleep 1
    redis-cli -p "$REDIS_Q_PORT" ping &>/dev/null && success "Redis queue started" \
        || { error "Redis queue failed"; exit 1; }
fi

# ── 4. Clear cache ────────────────────────────────────────────
info "Clearing Frappe cache..."
"$BENCH_BIN" --site "$SITE_NAME" clear-cache &>/dev/null \
    && success "Cache cleared" || warn "Cache clear skipped"

# ── 5. Web server ─────────────────────────────────────────────
info "Starting web server (port $PORT)..."
pkill -f "frappe serve --port $PORT" 2>/dev/null || true
sleep 1

OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES \
    "$BENCH_BIN" serve --port "$PORT" \
    >> "$LOG_DIR/web.log" 2>&1 &
WEB_PID=$!
save_pid $WEB_PID "web"

# Wait up to 20s for server to respond
for i in $(seq 1 20); do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT 2>/dev/null || echo "000")
    if [[ "$STATUS" =~ ^(200|301|302)$ ]]; then
        success "Web server started (PID $WEB_PID)"
        break
    fi
    sleep 1
    if [[ $i -eq 20 ]]; then
        error "Web server failed. Check: tail -f $LOG_DIR/web.log"
        exit 1
    fi
done

# ── 6. Worker ─────────────────────────────────────────────────
info "Starting background worker..."
pkill -f "frappe worker" 2>/dev/null || true; sleep 0.5

OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES NO_PROXY='*' \
    "$BENCH_BIN" worker >> "$LOG_DIR/worker.log" 2>&1 &
save_pid $! "worker"
success "Worker started"

# ── 7. Scheduler ──────────────────────────────────────────────
info "Starting scheduler..."
pkill -f "frappe schedule" 2>/dev/null || true; sleep 0.5

"$BENCH_BIN" schedule >> "$LOG_DIR/scheduler.log" 2>&1 &
save_pid $! "scheduler"
success "Scheduler started"

# ── 8. Public Tunnel ──────────────────────────────────────────
info "Setting up public tunnel..."
pkill -f "cloudflared tunnel" 2>/dev/null || true
pkill -f "ngrok http"         2>/dev/null || true
sleep 1
TUNNEL_URL=""

# ── Option A: ngrok static domain (permanent URL) ────────────
if command -v ngrok &>/dev/null && [[ -n "$NGROK_AUTHTOKEN" && -n "$NGROK_STATIC_DOMAIN" ]]; then
    info "Starting ngrok with static domain: $NGROK_STATIC_DOMAIN"
    ngrok http "$PORT" \
        --domain="$NGROK_STATIC_DOMAIN" \
        --log=stdout \
        > "$LOG_DIR/ngrok.log" 2>&1 &
    save_pid $! "cloudflare"   # reuse slot

    # Wait for ngrok to confirm it's running
    for i in $(seq 1 15); do
        if curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -q "public_url"; then
            TUNNEL_URL="https://$NGROK_STATIC_DOMAIN"
            break
        fi
        sleep 1
    done

    if [[ -n "$TUNNEL_URL" ]]; then
        success "ngrok tunnel active — PERMANENT URL"
    else
        warn "ngrok tunnel slow to start — URL: https://$NGROK_STATIC_DOMAIN"
        TUNNEL_URL="https://$NGROK_STATIC_DOMAIN"
    fi

# ── Option B: cloudflared quick tunnel (temporary URL) ────────
elif command -v cloudflared &>/dev/null; then
    TUNNEL_LOG="/tmp/artech-tunnel.log"
    cloudflared tunnel --url http://localhost:$PORT \
        > "$TUNNEL_LOG" 2>&1 &
    save_pid $! "cloudflare"

    warn "Using temporary Cloudflare URL (changes on restart)"
    info "For a PERMANENT URL → add ngrok credentials to .env"

    for i in $(seq 1 30); do
        TUNNEL_URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' "$TUNNEL_LOG" 2>/dev/null | tail -1 || true)
        [[ -n "$TUNNEL_URL" ]] && break
        sleep 1
    done
fi

# Save URL to file
[[ -n "$TUNNEL_URL" ]] && echo "$TUNNEL_URL" > "$TUNNEL_URL_FILE"

# ── Done ──────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════${RESET}"
echo -e "${BOLD}  ✅  Artech ERP is LIVE!${RESET}"
echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════${RESET}"
echo ""
echo -e "  ${BOLD}Login        :${RESET}  Administrator / (your admin password)"
echo -e "  ${BOLD}Local URL    :${RESET}  http://localhost:$PORT"

if [[ -n "$TUNNEL_URL" ]]; then
    if [[ -n "$NGROK_STATIC_DOMAIN" ]]; then
        echo -e "  ${BOLD}Public URL   :${RESET}  ${CYAN}${BOLD}$TUNNEL_URL${RESET}  ${GREEN}← PERMANENT${RESET}"
    else
        echo -e "  ${BOLD}Public URL   :${RESET}  ${CYAN}${BOLD}$TUNNEL_URL${RESET}  ${YELLOW}← changes on restart${RESET}"
        echo ""
        echo -e "  ${YELLOW}  → For a permanent URL, add these to .env:${RESET}"
        echo -e "  ${YELLOW}    NGROK_AUTHTOKEN=<your-token>${RESET}"
        echo -e "  ${YELLOW}    NGROK_STATIC_DOMAIN=<your-domain>.ngrok-free.app${RESET}"
        echo -e "  ${YELLOW}    Sign up FREE: https://ngrok.com${RESET}"
    fi
else
    warn "Tunnel URL not ready. Check logs."
fi

echo ""
echo -e "  ${BOLD}Logs dir     :${RESET}  $LOG_DIR/"
echo -e "  ${BOLD}Stop         :${RESET}  ./artech-start.sh stop"
echo -e "  ${BOLD}Status       :${RESET}  ./artech-start.sh status"
echo ""
echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════${RESET}"
echo ""

# ── Watch for tunnel URL changes in background ────────────────
if [[ -z "$NGROK_STATIC_DOMAIN" ]]; then
    TUNNEL_LOG="${TUNNEL_LOG:-/tmp/artech-tunnel.log}"
    (   while true; do
            NEW_URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' "$TUNNEL_LOG" 2>/dev/null | tail -1 || true)
            if [[ -n "$NEW_URL" && "$NEW_URL" != "$(cat "$TUNNEL_URL_FILE" 2>/dev/null)" ]]; then
                echo "$NEW_URL" > "$TUNNEL_URL_FILE"
                echo -e "\n  ${YELLOW}⚡ New tunnel URL → ${CYAN}${BOLD}$NEW_URL${RESET}"
            fi
            sleep 15
        done
    ) &
fi
