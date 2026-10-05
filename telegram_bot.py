"""
Telegram Channel Publisher for AffiliateDealPro.
Sends formatted deal alerts with photo captions and inline affiliate buttons.
"""

from __future__ import annotations
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional, Tuple


class TelegramDealPublisher:
    def __init__(self, bot_token: str, channel_id: str, footer: str = ""):
        self.bot_token = bot_token.strip()
        self.channel_id = channel_id.strip()
        self.footer = footer
        self.api_base = f"https://api.telegram.org/bot{self.bot_token}"

    def is_configured(self) -> bool:
        return bool(self.bot_token and self.channel_id and "YOUR_" not in self.bot_token)

    def test_connection(self) -> Tuple[bool, str]:
        """Test if the bot token is valid."""
        if not self.is_configured():
            return False, "Chưa cấu hình Telegram Bot Token hoặc Channel ID."

        url = f"{self.api_base}/getMe"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AffiliateDealPro/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("ok"):
                    bot_name = data.get("result", {}).get("username", "UnknownBot")
                    return True, f"Kết nối Bot thành công: @{bot_name}"
                return False, f"Lỗi từ Telegram: {data.get('description')}"
        except Exception as e:
            return False, f"Không thể kết nối Telegram: {e}"

    def format_deal_caption(self, deal: Dict[str, Any]) -> str:
        """Create eye-catching HTML caption for the deal post."""
        title = deal.get("title", "Sản phẩm giảm giá sốc")
        orig_price = deal.get("original_price_formatted", "---")
        sale_price = deal.get("sale_price_formatted", "---")
        discount = deal.get("discount_percent", 0)
        rating = deal.get("rating", 5.0)
        sold = deal.get("sold_count", "")
        voucher = deal.get("voucher_code", "")

        caption_lines = [
            f"🔥 <b>DEAL HOT GIẢM {discount}%</b> 🔥",
            "",
            f"📦 <b>{title}</b>",
            "",
            f"💵 <b>Giá sale:</b> <code>{sale_price}</code>",
            f"🏷️ <b>Giá gốc:</b> <s>{orig_price}</s> (Tiết kiệm cực hời!)",
        ]

        if rating:
            rating_stars = "⭐" * int(min(5, max(1, round(rating))))
            caption_lines.append(f"⭐ <b>Đánh giá:</b> {rating:.1f}/5.0 {rating_stars}")

        if sold:
            caption_lines.append(f"🛒 <b>Đã bán:</b> {sold}")

        if voucher:
            caption_lines.append(f"🎟️ <b>Mã giảm giá:</b> <code>{voucher}</code>")

        if self.footer:
            caption_lines.extend(["", f"<i>{self.footer}</i>"])

        return "\n".join(caption_lines)

    def publish_deal(self, deal: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Send deal to Telegram channel with inline button.
        """
        if not self.is_configured():
            return False, "Bot chưa được cấu hình token hoặc channel."

        caption = self.format_deal_caption(deal)
        affiliate_url = deal.get("affiliate_url", "") or deal.get("url", "")
        discount = deal.get("discount_percent", 0)
        button_text = f"🛒 MUA NGAY (GIẢM {discount}%)"

        inline_keyboard = {
            "inline_keyboard": [
                [{"text": button_text, "url": affiliate_url}]
            ]
        }

        image_url = deal.get("image_url", "")
        
        # Try sending photo with caption first
        if image_url and image_url.startswith("http"):
            photo_payload = {
                "chat_id": self.channel_id,
                "photo": image_url,
                "caption": caption,
                "parse_mode": "HTML",
                "reply_markup": json.dumps(inline_keyboard)
            }
            success, msg = self._send_request("sendPhoto", photo_payload)
            if success:
                return True, msg

        # Fallback to sendMessage if photo fails or no image
        msg_payload = {
            "chat_id": self.channel_id,
            "text": caption,
            "parse_mode": "HTML",
            "reply_markup": json.dumps(inline_keyboard),
            "disable_web_page_preview": False
        }
        return self._send_request("sendMessage", msg_payload)

    def _send_request(self, method: str, data: Dict[str, Any]) -> Tuple[bool, str]:
        url = f"{self.api_base}/{method}"
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(url, data=encoded_data, headers={
            "User-Agent": "AffiliateDealPro/1.0",
            "Content-Type": "application/x-www-form-urlencoded"
        })

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                res_json = json.loads(resp.read().decode("utf-8"))
                if res_json.get("ok"):
                    return True, "Gửi tin nhắn Telegram thành công!"
                return False, f"Lỗi Telegram: {res_json.get('description')}"
        except Exception as e:
            return False, f"Lỗi kết nối Telegram ({method}): {e}"
