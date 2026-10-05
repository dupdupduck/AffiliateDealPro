#!/usr/bin/env python3
"""
AffiliateDealPro — Autonomous High-Discount Deal Hunter & Auto-Affiliate Publisher.
Scans Flash Sales, converts URLs to affiliate links, and posts formatted deals to Telegram.
"""

from __future__ import annotations
import argparse
import datetime
import os
import sys
import time
from typing import Dict, Any

from config import load_config, save_config
from deal_hunter import DealHunter
from affiliate import AffiliateConverter
from telegram_bot import TelegramDealPublisher
import tui


def run_setup_wizard() -> None:
    """Interactive wizard to configure bot tokens and affiliate IDs."""
    tui.clear_screen()
    tui.print_banner()
    print(f"{tui.C_BOLD}⚙️  HƯỚNG DẪN CẤU HÌNH NHANH CHO BOT AFFILIATE{tui.C_RESET}\n")

    current_config = load_config()

    token = input(f"1. Nhập Telegram Bot Token [{current_config.get('telegram_bot_token')}]: ").strip()
    if token:
        current_config["telegram_bot_token"] = token

    channel = input(f"2. Nhập Telegram Channel ID (Ví dụ: @kenh_san_deal hoặc -100xxxxxxx) [{current_config.get('telegram_channel_id')}]: ").strip()
    if channel:
        current_config["telegram_channel_id"] = channel

    sub_id = input(f"3. Nhập mã Affiliate Tracking SubID [{current_config.get('affiliate_sub_id')}]: ").strip()
    if sub_id:
        current_config["affiliate_sub_id"] = sub_id

    min_disc_str = input(f"4. Mức giảm giá tối thiểu để lọc (%) [{current_config.get('min_discount_percent', 30)}]: ").strip()
    if min_disc_str.isdigit():
        current_config["min_discount_percent"] = int(min_disc_str)

    save_config(current_config)
    print(f"\n{tui.C_GREEN}✅ Cấu hình đã được lưu vào file config.json thành công!{tui.C_RESET}\n")


def run_single_cycle(
    hunter: DealHunter,
    converter: AffiliateConverter,
    publisher: TelegramDealPublisher,
    config: Dict[str, Any],
    stats: Dict[str, Any],
    dry_run: bool = False
) -> None:
    """Execute one scan and publish cycle."""
    max_posts = config.get("max_posts_per_cycle", 3)
    deals = hunter.fetch_live_deals()
    stats["scanned"] += len(deals)
    stats["last_run"] = datetime.datetime.now().strftime("%H:%M:%S")

    qualified = [d for d in deals if not hunter.is_already_posted(d["id"])]
    stats["qualified"] += len(qualified)

    posted_count = 0
    for deal in qualified:
        if posted_count >= max_posts:
            break

        # Convert URL to affiliate link
        deal["affiliate_url"] = converter.convert_url(deal.get("url", ""), deal.get("id", ""))

        if dry_run:
            tui.print_deal_card(deal)
            posted_count += 1
            stats["published"] += 1
            hunter.mark_as_posted(deal["id"], deal["title"], deal["discount_percent"])
        else:
            success, msg = publisher.publish_deal(deal)
            if success:
                posted_count += 1
                stats["published"] += 1
                hunter.mark_as_posted(deal["id"], deal["title"], deal["discount_percent"])
                print(f" {tui.C_GREEN}✓{tui.C_RESET} Đã đăng: {deal['title'][:40]}... (Giảm {deal['discount_percent']}%)")
                time.sleep(3)  # Respect Telegram rate-limits
            else:
                print(f" {tui.C_RED}✗{tui.C_RESET} Gửi lỗi: {msg}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AffiliateDealPro — Autonomous High-Discount Deal Hunter & Auto-Affiliate Publisher"
    )
    parser.add_argument("--setup", action="store_true", help="Chạy trình hướng dẫn cài đặt cấu hình")
    parser.add_argument("--test", action="store_true", help="Quét và hiển thị deal mẫu ra màn hình (không gửi Telegram)")
    parser.add_argument("--send-test", action="store_true", help="Gửi 1 deal thử nghiệm lên Telegram để kiểm tra bot")
    args = parser.parse_args()

    if args.setup:
        run_setup_wizard()
        return

    config = load_config()
    hunter = DealHunter(config)
    converter = AffiliateConverter(config)
    publisher = TelegramDealPublisher(
        bot_token=config.get("telegram_bot_token", ""),
        channel_id=config.get("telegram_channel_id", ""),
        footer=config.get("channel_footer", "")
    )

    tui.clear_screen()
    tui.print_banner()

    stats: Dict[str, Any] = {
        "scanned": 0,
        "qualified": 0,
        "published": 0,
        "last_run": "Đang khởi động...",
        "bot_connected": False
    }

    # Verify Telegram bot connection
    if publisher.is_configured():
        ok, msg = publisher.test_connection()
        stats["bot_connected"] = ok
        if ok:
            print(f"{tui.C_GREEN}✓ {msg}{tui.C_RESET}")
        else:
            print(f"{tui.C_YELLOW}⚠️  {msg}{tui.C_RESET}")
    else:
        print(f"{tui.C_YELLOW}💡 Mẹo: Chạy 'python main.py --setup' để kết nối Telegram Bot của bạn.{tui.C_RESET}")

    if args.test:
        print(f"\n{tui.C_CYAN}🔍 Đang chạy chế độ kiểm tra dữ liệu (--test)...{tui.C_RESET}\n")
        run_single_cycle(hunter, converter, publisher, config, stats, dry_run=True)
        print(f"\n{tui.C_GREEN}Hoàn tất kiểm tra! Các deal trên đã được gắn link Affiliate thành công.{tui.C_RESET}\n")
        return

    if args.send_test:
        print(f"\n{tui.C_CYAN}📤 Đang gửi 1 deal kiểm tra lên kênh Telegram...{tui.C_RESET}\n")
        sample_deals = hunter.fetch_live_deals()
        if sample_deals:
            d = sample_deals[0]
            d["affiliate_url"] = converter.convert_url(d.get("url", ""), d.get("id", ""))
            ok, msg = publisher.publish_deal(d)
            if ok:
                print(f"{tui.C_GREEN}✓ Gửi thành công lên {config.get('telegram_channel_id')}! Hãy mở Telegram để kiểm tra.{tui.C_RESET}\n")
            else:
                print(f"{tui.C_RED}✗ Lỗi gửi tin: {msg}{tui.C_RESET}\n")
        return

    # Daemon Autonomous Loop
    interval = config.get("check_interval_seconds", 1800)
    print(f"\n{tui.C_GREEN}🚀 Hệ thống săn deal tự động bắt đầu hoạt động! (Chu kỳ: {interval // 60} phút){tui.C_RESET}")
    print(f"{tui.C_DIM}Nhấn Ctrl + C để dừng bot bất cứ lúc nào.{tui.C_RESET}\n")

    try:
        while True:
            tui.clear_screen()
            tui.print_banner()
            tui.print_dashboard_status(stats, config)

            print(f"{tui.C_CYAN}🔄 Đang quét deal mới nhất trên sàn thương mại...{tui.C_RESET}")
            run_single_cycle(hunter, converter, publisher, config, stats, dry_run=not publisher.is_configured())

            print(f"\n{tui.C_DIM}Đang chờ lượt quét tiếp theo trong {interval} giây...{tui.C_RESET}")
            for remaining in range(interval, 0, -1):
                sys.stdout.write(f"\r⏳ Quét lượt kế tiếp sau: {remaining // 60:02d}:{remaining % 60:02d}s  ")
                sys.stdout.flush()
                time.sleep(1)
            print()

    except KeyboardInterrupt:
        print(f"\n\n{tui.C_YELLOW}🛑 Đã tạm dừng bot AffiliateDealPro. Hẹn gặp lại bạn!{tui.C_RESET}\n")


if __name__ == "__main__":
    main()
