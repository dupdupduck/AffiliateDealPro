#!/usr/bin/env bash
# ========================================================
# AffiliateDealPro — One-Click Installer for Termux & Linux
# ========================================================

set -e

echo -e "\033[1;36m"
cat << "EOF"
   ___   __  ___ __ _       __       ___             
  / _ | / _/ _/ // /(_)__ _/ /____  / _ \_______    
 / __ |/ _// _/ // // / _ `/ __/ -_) / ___/ __/ _ \   
/_/ |_/_/ /_/ /_//_//_/\_,_/\__/\__/ /_/  /_/  \___/   
EOF
echo -e "\033[1;35m>> Setting up AffiliateDealPro Environment... <<\033[0m\n"

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo -e "\033[1;33m[!] Python3 is not installed. Installing...\033[0m"
    if [ -d "/data/data/com.termux" ]; then
        pkg update -y && pkg install python -y
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3 python3-pip
    fi
fi

# Install dependencies
echo -e "\033[1;32m[+] Installing required Python packages...\033[0m"
pip install -r requirements.txt || python3 -m pip install -r requirements.txt

# Create initial config if not exists
if [ ! -f "config.json" ]; then
    echo -e "\033[1;34m[+] Creating default config.json from example...\033[0m"
    cp config.example.json config.json
fi

chmod +x main.py

echo -e "\n\033[1;32m[✓] Installation completed successfully!\033[0m"
echo -e "\033[1;36mTo configure your Telegram Bot and Affiliate ID, run:\033[0m"
echo -e "    python3 main.py --setup\n"
echo -e "\033[1;36mTo start hunting and broadcasting deals, run:\033[0m"
echo -e "    python3 main.py\n"
