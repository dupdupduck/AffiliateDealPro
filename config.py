"""
Configuration management for AffiliateDealPro.
Loads settings from config.json with environment variable overrides.
"""

from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG_PATH = Path(__file__).parent / "config.json"
EXAMPLE_CONFIG_PATH = Path(__file__).parent / "config.example.json"

DEFAULT_SETTINGS: Dict[str, Any] = {
    "telegram_bot_token": "",
    "telegram_channel_id": "",
    "affiliate_sub_id": "my_affiliate_id",
    "affiliate_platform": "shopee",
    "custom_affiliate_prefix": "https://s.shopee.vn/universal-link?sub_id=",
    "min_discount_percent": 30,
    "check_interval_seconds": 1800,
    "max_posts_per_cycle": 3,
    "enable_mock_fallback": True,
    "channel_footer": "🔔 Bật thông báo kênh để không bỏ lỡ deal hời mỗi ngày!",
}


def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """Load config from JSON file or return defaults with env overrides."""
    config = dict(DEFAULT_SETTINGS)

    if config_path.is_file():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                saved = json.load(f)
                config.update(saved)
        except Exception as e:
            print(f"⚠️ [Config] Không thể đọc {config_path}: {e}. Sử dụng cấu hình mặc định.")

    # Environment variable overrides
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        config["telegram_bot_token"] = os.getenv("TELEGRAM_BOT_TOKEN")
    if os.getenv("TELEGRAM_CHANNEL_ID"):
        config["telegram_channel_id"] = os.getenv("TELEGRAM_CHANNEL_ID")
    if os.getenv("AFFILIATE_SUB_ID"):
        config["affiliate_sub_id"] = os.getenv("AFFILIATE_SUB_ID")

    return config


def save_config(config: Dict[str, Any], config_path: Path = DEFAULT_CONFIG_PATH) -> None:
    """Save config dictionary to JSON file."""
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
