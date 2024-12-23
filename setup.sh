#!/bin/bash
echo "Enter server address (IP):"
# shellcheck disable=SC2162
read SERVER_ADDRESS
echo "Enter Telegram token:"
# shellcheck disable=SC2162
read TOKEN

if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

if ! command -v docker-compose &> /dev/null && ! command -v docker compose &> /dev/null; then
    echo "Docker Compose not found. Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

cat <<EOF > .env
PUID=1000
PGID=1000
TZ=Europe/Moscow
SERVERURL="$SERVER_ADDRESS"
SERVERPORT=51820
PEERS=0
PEERDNS=true
INTERNAL_SUBNET=10.13.13.0
PYTHONUNBUFFERED=1             # don't touch me pls
PYTHONDONTWRITEBYTECODE=1      # don't touch me pls
EOF

if [ -f .env ]; then
    echo "File .env created successfully:"
else
    echo "Error: .env file creation failed."
fi

mkdir -p secrets

echo -n "$TOKEN" > secrets/telegram-token.txt

echo "File secrets/telegram-token.txt created successfully."
