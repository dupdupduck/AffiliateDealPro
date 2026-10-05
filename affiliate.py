"""
Affiliate URL Converter & Tracking Engine.
Transforms standard e-commerce URLs into monetized affiliate referral links.
"""

from __future__ import annotations
import urllib.parse
from typing import Dict, Any


class AffiliateConverter:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sub_id = config.get("affiliate_sub_id", "dealpro")
        self.platform = config.get("affiliate_platform", "shopee").lower()
        self.custom_prefix = config.get("custom_affiliate_prefix", "")

    def convert_url(self, raw_url: str, product_id: str = "") -> str:
        """
        Convert product URL to user's affiliate link with sub_id tracking.
        """
        if not raw_url:
            return ""

        # If custom prefix is configured and url is relative
        if self.custom_prefix and not raw_url.startswith("http"):
            return f"{self.custom_prefix}{self.sub_id}&url={urllib.parse.quote(raw_url)}"

        parsed = urllib.parse.urlparse(raw_url)
        query = urllib.parse.parse_qs(parsed.query)

        # Shopee affiliate tracking parameters
        if "shopee" in parsed.netloc or self.platform == "shopee":
            query["utm_source"] = ["affiliate"]
            query["utm_medium"] = ["deal_hunter_bot"]
            query["utm_campaign"] = [self.sub_id]
            query["sub_id"] = [self.sub_id]
            query["aff_source"] = ["affiliate_deal_pro"]

        # Lazada affiliate tracking parameters
        elif "lazada" in parsed.netloc or self.platform == "lazada":
            query["aff_sub"] = [self.sub_id]
            query["exlaz"] = [f"d_1:mm_affiliate_sub_{self.sub_id}"]

        # Reconstruct URL with tracking tags
        new_query = urllib.parse.urlencode(query, doseq=True)
        affiliate_url = urllib.parse.urlunparse((
            parsed.scheme or "https",
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))

        return affiliate_url
