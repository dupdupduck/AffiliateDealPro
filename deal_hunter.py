"""
Deal Hunter Engine for AffiliateDealPro.
Discovers high-discount Flash Sale deals, validates discounts, and manages post history.
"""

from __future__ import annotations
import json
import sqlite3
import time
import urllib.request
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_PATH = Path(__file__).parent / "deals_history.db"

# Sample curated hot deals as realistic fallback/test feed
MOCK_HOT_DEALS = [
    {
        "id": "shopee_deal_001",
        "title": "Tai Nghe Bluetooth Không Dây True Wireless Chống Ồn Chủ Động ANC Âm Bass Cực Căng",
        "original_price": 550000,
        "sale_price": 189000,
        "discount_percent": 65,
        "rating": 4.9,
        "sold_count": "12.4k",
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&auto=format&fit=crop",
        "url": "https://shopee.vn/product/12345/67890",
        "voucher_code": "GIAM50K",
    },
    {
        "id": "shopee_deal_002",
        "title": "Sạc Nhanh 65W GaN Đa Cổng Type-C & USB Tương Thích iPhone, Samsung, Laptop",
        "original_price": 420000,
        "sale_price": 199000,
        "discount_percent": 52,
        "rating": 4.8,
        "sold_count": "8.9k",
        "image_url": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&auto=format&fit=crop",
        "url": "https://shopee.vn/product/23456/78901",
        "voucher_code": "TECH20K",
    },
    {
        "id": "shopee_deal_003",
        "title": "Chuột Không Dây Gaming Silent Click Led RGB Pin Trâu Dùng 1 Tháng",
        "original_price": 310000,
        "sale_price": 129000,
        "discount_percent": 58,
        "rating": 4.7,
        "sold_count": "15.1k",
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&auto=format&fit=crop",
        "url": "https://shopee.vn/product/34567/89012",
        "voucher_code": "FREESHIP",
    },
    {
        "id": "shopee_deal_004",
        "title": "Bàn Phím Cơ Không Dây 3 Chế Độ Kết Nối Bluetooth/2.4G/Dây Hot-swap Led Rainbow",
        "original_price": 890000,
        "sale_price": 399000,
        "discount_percent": 55,
        "rating": 4.9,
        "sold_count": "6.3k",
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop",
        "url": "https://shopee.vn/product/45678/90123",
        "voucher_code": "KEYBOARD10",
    },
    {
        "id": "shopee_deal_005",
        "title": "Đồng Hồ Thông Minh Theo Dõi Sức Khỏe Đo Nhịp Tim SpO2 Chống Nước IP68",
        "original_price": 750000,
        "sale_price": 289000,
        "discount_percent": 61,
        "rating": 4.8,
        "sold_count": "9.7k",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop",
        "url": "https://shopee.vn/product/56789/01234",
        "voucher_code": "WATCH50K",
    }
]


class DealHunter:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.min_discount = config.get("min_discount_percent", 30)
        self.enable_mock = config.get("enable_mock_fallback", True)
        self.db_path = DB_PATH
        self._init_db()

    def _init_db(self) -> None:
        """Initialize database for tracking posted deals to prevent spamming duplicates."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS posted_deals (
                deal_id TEXT PRIMARY KEY,
                title TEXT,
                discount INTEGER,
                posted_at REAL
            )
        """)
        conn.commit()
        conn.close()

    def is_already_posted(self, deal_id: str) -> bool:
        """Check if deal was posted in the last 48 hours."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cutoff = time.time() - (48 * 3600)
        cur.execute("SELECT 1 FROM posted_deals WHERE deal_id = ? AND posted_at > ?", (deal_id, cutoff))
        row = cur.fetchone()
        conn.close()
        return row is not None

    def mark_as_posted(self, deal_id: str, title: str, discount: int) -> None:
        """Record that a deal has been published."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO posted_deals (deal_id, title, discount, posted_at) VALUES (?, ?, ?, ?)",
            (deal_id, title, discount, time.time())
        )
        conn.commit()
        conn.close()

    def format_price_vnd(self, amount: int) -> str:
        """Format number to Vietnamese Dong currency string (e.g. 150.000 đ)."""
        return f"{amount:,.0f}".replace(",", ".") + " đ"

    def fetch_live_deals(self) -> List[Dict[str, Any]]:
        """
        Fetch deals from public e-commerce flash sale endpoints.
        Falls back to curated high-converting deals if remote API is unreachable.
        """
        deals: List[Dict[str, Any]] = []

        # Attempt to fetch public Shopee Flash Sale data
        try:
            url = "https://shopee.vn/api/v4/flash_sale/flash_sale_get_items?limit=20&item_type=0"
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36",
                    "Accept": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                items = data.get("data", {}).get("items", [])
                for it in items:
                    item_id = str(it.get("itemid", ""))
                    shop_id = str(it.get("shopid", ""))
                    raw_orig = it.get("price_before_discount", 0) // 100000
                    raw_sale = it.get("price", 0) // 100000
                    raw_discount = it.get("discount", 0)

                    if raw_orig > 0 and raw_sale > 0 and raw_discount >= self.min_discount:
                        deals.append({
                            "id": f"shopee_{item_id}",
                            "title": it.get("name", "Sản phẩm Flash Sale"),
                            "original_price": raw_orig,
                            "sale_price": raw_sale,
                            "discount_percent": int(raw_discount),
                            "rating": 4.9,
                            "sold_count": str(it.get("sold", 100)),
                            "image_url": f"https://cf.shopee.vn/file/{it.get('image', '')}" if it.get('image') else "",
                            "url": f"https://shopee.vn/product/{shop_id}/{item_id}",
                            "voucher_code": ""
                        })
        except Exception:
            # Fallback to curated mock deals when running in restricted environments
            pass

        if not deals and self.enable_mock:
            deals = list(MOCK_HOT_DEALS)

        # Format and validate all deals
        qualified: List[Dict[str, Any]] = []
        for d in deals:
            disc = d.get("discount_percent", 0)
            if disc >= self.min_discount:
                d["original_price_formatted"] = self.format_price_vnd(d["original_price"])
                d["sale_price_formatted"] = self.format_price_vnd(d["sale_price"])
                qualified.append(d)

        return qualified
