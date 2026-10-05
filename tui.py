"""
Terminal User Interface (TUI) & Dashboard for AffiliateDealPro.
Displays neon banners, live execution metrics, and deal inspection tables.
"""

from __future__ import annotations
import os
import sys
import time
from typing import Dict, Any, List

# ANSI Color Codes
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_MAGENTA = "\033[95m"
C_BLUE = "\033[94m"
C_BG_DARK = "\033[40m"


def clear_screen() -> None:
    os.system("clear" if os.name != "nt" else "cls")


def print_banner() -> None:
    banner = (
        f"{C_CYAN}{C_BOLD}"
        r"""   ___   __  ___ __ _       __       ___             
  / _ | / _/ _/ // /(_)__ _/ /____  / _ \_______    
 / __ |/ _// _/ // // / _ `/ __/ -_) / ___/ __/ _ \   
/_/ |_/_/ /_/ /_//_//_/\_,_/\__/\__/ /_/  /_/  \___/   """
        f"\n{C_MAGENTA}   >> Autonomous E-Commerce Deal Hunter & Affiliate Bot <<{C_RESET}\n"
        f"{C_DIM}         (Shopee / Lazada / Telegram Auto-Publisher){C_RESET}\n"
    )
    print(banner)


def print_dashboard_status(stats: Dict[str, Any], config: Dict[str, Any]) -> None:
    bot_status = f"{C_GREEN}ĐÃ KẾT NỐI{C_RESET}" if stats.get("bot_connected") else f"{C_YELLOW}CHƯA CẤU HÌNH TOKEN{C_RESET}"
    channel = config.get("telegram_channel_id") or "Chưa đặt"
    sub_id = config.get("affiliate_sub_id") or "Mặc định"
    min_disc = config.get("min_discount_percent", 30)

    print(f"{C_BOLD}┌── [ TRẠNG THÁI HỆ THỐNG ] ──────────────────────────────────────────┐{C_RESET}")
    print(f"│ 🤖 Telegram Bot:   {bot_status:<36}│")
    print(f"│ 📢 Kênh đăng tin:  {C_CYAN}{channel:<47}{C_RESET}│")
    print(f"│ 🏷️  Affiliate ID:   {C_MAGENTA}{sub_id:<47}{C_RESET}│")
    print(f"│ 🎯 Giảm giá tối thiểu: {C_YELLOW}>{min_disc}%{'':<43}{C_RESET}│")
    print(f"├─────────────────────────────────────────────────────────────────────┤")
    print(f"│ 📊 Tổng deal đã quét:     {C_BOLD}{stats.get('scanned', 0):<41}{C_RESET}│")
    print(f"│ ✅ Deal đạt chuẩn (>={min_disc}%): {C_GREEN}{C_BOLD}{stats.get('qualified', 0):<41}{C_RESET}│")
    print(f"│ 🚀 Đã gửi lên Telegram:   {C_CYAN}{C_BOLD}{stats.get('published', 0):<41}{C_RESET}│")
    print(f"│ ⏱️ Lần quét gần nhất:     {stats.get('last_run', 'Vừa khởi động'):<41}│")
    print(f"{C_BOLD}└─────────────────────────────────────────────────────────────────────┘{C_RESET}")
    print()


def print_deal_card(deal: Dict[str, Any]) -> None:
    """Print a single deal in a stylish terminal card."""
    title = deal.get("title", "")
    if len(title) > 60:
        title = title[:57] + "..."

    discount = deal.get("discount_percent", 0)
    sale_p = deal.get("sale_price_formatted", "")
    orig_p = deal.get("original_price_formatted", "")
    aff_url = deal.get("affiliate_url", "")

    print(f"{C_YELLOW}╔═══ [ DEAL HOT: GIẢM {discount}% ] ═════════════════════════════════════════╗{C_RESET}")
    print(f"║ 📦 {C_BOLD}{title:<64}{C_RESET}║")
    print(f"║ 💵 Giá sale: {C_GREEN}{C_BOLD}{sale_p:<15}{C_RESET} Giá gốc: {C_DIM}{orig_p:<28}{C_RESET}║")
    print(f"║ 🔗 Link: {C_CYAN}{aff_url[:60]:<60}{C_RESET}║")
    print(f"{C_YELLOW}╚══════════════════════════════════════════════════════════════════════╝{C_RESET}")
