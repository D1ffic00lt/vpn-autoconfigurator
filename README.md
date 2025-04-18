# VPN Autoconfigurator

<div align="center">

<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/D1ffic00lt/vpn-autoconfigurator">
<img alt="GitHub code size" src="https://img.shields.io/github/languages/code-size/D1ffic00lt/vpn-autoconfigurator">
<img alt="GitHub commits stats" src="https://img.shields.io/github/commit-activity/y/D1ffic00lt/vpn-autoconfigurator">
<img alt="GitHub License" src="https://img.shields.io/github/license/D1ffic00lt/vpn-autoconfigurator">

</div>

> WireGuard‑based VPN stack shipped as Docker Compose. **One‑command deploy** or build‑from‑source – your choice.

---

## Features

* **Interactive setup script** – installs Docker/Compose if missing and writes `.env` & secrets.
* **Priority registry: GitHub Container Registry (GHCR)** – images are published here first; Docker Hub acts as a fallback.
* Local build option via `docker-compose.local.yml` for complete transparency.
* Telegram bot integration for peer creation and status alerts.
* Optional `nice ‑20` launch for real‑time scheduling.
* Release archives downloadable from the GitHub Releases page.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Linux x86_64/arm64 | Tested on Ubuntu 22.04 and Debian 12 |
| Root or `sudo` rights | Needed for Docker install & `nice -20` |
| `bash` | `setup.sh` uses Bash‑specific syntax |

The `setup.sh` script installs **Docker Engine** and **Docker Compose** automatically when absent.

---

## Quick Start

### Option 1 – Clone the repository

```bash
# 1 · Grab the code
git clone https://github.com/D1ffic00lt/vpn-autoconfigurator.git
cd vpn-autoconfigurator

# 2 · Run the interactive setup (one‑time)
chmod +x ./setup.sh
./setup.sh
```

### Option 2 – Download the latest release archive

```bash
curl -L "https://github.com/D1ffic00lt/vpn-autoconfigurator/releases/latest/download/vpn-autoconfigurator.tar.gz" -o vpn-autoconfigurator.tar.gz

tar -xzf vpn-autoconfigurator.tar.gz
cd vpn-autoconfigurator
chmod +x ./setup.sh
./setup.sh
```

### Option 3 – **Build from source (local images)**

Prefer this path if you want to avoid pulling pre‑built images:

```bash
# Clone & configure
git clone https://github.com/D1ffic00lt/vpn-autoconfigurator.git
cd vpn-autoconfigurator
chmod +x ./setup.sh
./setup.sh            # generates .env and secrets

# Build and run using local Dockerfiles
docker-compose -f docker-compose.local.yml build

docker-compose -f docker-compose.local.yml up -d
```

During setup you will be prompted for:

1. **Server address** – public IP or domain name of the host.
2. **Telegram bot token** – used to deliver client configs & status messages.

After completion you will have:

* `.env` – environment overrides for Compose
* `secrets/telegram-token.txt` – secure storage of the Telegram token

---

## Starting the Stack

### Highest priority (nice ‑20)

| Registry (preferred → fallback) | Command |
|---------------------------------|---------|
| **GHCR** | `sudo nice -n -20 docker-compose -f docker-compose.ghcr.yml up -d` |
| Docker Hub | `sudo nice -n -20 docker-compose -f docker-compose.yml up -d` |

### Normal priority

| Registry (preferred → fallback) | Command |
|---------------------------------|---------|
| **GHCR** | `docker-compose -f docker-compose.ghcr.yml up -d` |
| Docker Hub | `docker-compose -f docker-compose.yml up -d` |

> **Tip:** With Docker Compose v2 you can replace `docker-compose` with `docker compose`.

---

## Updating

```bash
docker-compose pull
docker-compose up -d
```

---

## Stopping

```bash
docker-compose down
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUID` | `1000` | Host user ID for file ownership |
| `PGID` | `1000` | Host group ID |
| `TZ` | `Europe/Moscow` | Time zone inside the containers |
| `SERVERURL` | — | Public hostname or IP address |
| `SERVERPORT` | `51820` | UDP port WireGuard listens on |
| `PEERS` | `0` | Number of peers generated automatically |
| `PEERDNS` | `true` | Push DNS server to clients |
| `INTERNAL_SUBNET` | `10.13.13.0` | WireGuard subnet |

---

## Logs & Troubleshooting

```bash
# Real‑time logs
docker-compose logs -f

# Live CPU/RAM usage
docker stats
```

### Common Issues

* **Port 51820 already in use** – stop other WireGuard instances or change `SERVERPORT`.
* **Telegram messages not delivered** – verify the token and start the bot via `@BotFather`.

