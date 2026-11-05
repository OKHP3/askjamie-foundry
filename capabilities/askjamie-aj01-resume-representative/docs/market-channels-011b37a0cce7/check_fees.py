#!/usr/bin/env python3
"""Reproduce illustrative US channel economics; no network or account access.
Sources and exclusions are in research.md and sources.md. Each fee component
is rounded half up to cents before subtraction. Provider rounding may differ.
"""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import json

D = Decimal
CENT = D("0.01")
PRICES = (10, 49, 50, 75, 79, 99, 149, 179, 199, 200, 300)
COMPONENTS = {
    "ko_fi": (("0.05", "0"), ("0.029", "0.30")),
    "gumroad_direct": (("0.10", "0.50"), ("0.029", "0.30")),
    "gumroad_discover": (("0.30", "0"),),
    "fiverr_seller": (("0.20", "0"),),
    "etsy_eligible_only": (("0.065", "0"), ("0.03", "0.25"), ("0", "0.20")),
    "payhip_free": (("0.05", "0"), ("0.029", "0.30")),
}

def money(x: Decimal) -> Decimal:
    return x.quantize(CENT, rounding=ROUND_HALF_UP)

def net(price: Decimal, channel: str) -> Decimal:
    if price < 0:
        raise ValueError("price must be non-negative")
    return price - sum((money(price * D(rate) + D(fixed))
                        for rate, fixed in COMPONENTS[channel]), D(0))

def independent_cents(price: Decimal, channel: str) -> int:
    # Independent rational/integer arithmetic rather than Decimal helper reuse.
    cents = int(price * 100)
    fees = 0
    for rate, fixed in COMPONENTS[channel]:
        exact = cents * Fraction(rate) + 100 * Fraction(fixed)
        q, remainder = divmod(exact.numerator, exact.denominator)
        fees += q + int(2 * remainder >= exact.denominator)
    return cents - fees

def buyer_total(price: Decimal) -> Decimal:
    return price + money(price * D("0.055")) + (D("3.50") if price < 200 else D(0))

def verify() -> dict:
    rows = []
    checks = 0
    for p in PRICES:
        price = D(p)
        result = {"price_usd": f"{price:.2f}"}
        for channel in COMPONENTS:
            value = net(price, channel)
            assert int(value * 100) == independent_cents(price, channel), (p, channel)
            result[channel] = f"{value:.2f}"
            checks += 1
        result["fiverr_buyer_before_tax"] = f"{buyer_total(price):.2f}"
        rows.append(result)
    fixtures = [
        (net(D(50), "ko_fi"), D("45.75")),
        (net(D(50), "gumroad_direct"), D("42.75")),
        (net(D(50), "fiverr_seller"), D("40.00")),
        (net(D(50), "etsy_eligible_only"), D("44.80")),
        (net(D(75), "etsy_eligible_only"), D("67.42")),
        (net(D(179), "etsy_eligible_only"), D("161.54")),
        (buyer_total(D(50)), D("56.25")),
        (buyer_total(D(199)), D("213.45")),
        (buyer_total(D(200)), D("211.00")),
        (D(12) / D("0.05"), D("240")),
    ]
    for actual, expected in fixtures:
        assert actual == expected, (actual, expected)
    return {
        "result": "PASS",
        "formula_crosschecks": checks,
        "fixed_fixtures": len(fixtures),
        "assumptions": "USD, domestic card, no sales tax/FX/ads/refunds/payout charges/monthly subscription; fee components rounded half up. Etsy is hypothetical for eligible products only.",
        "rows": rows,
    }

if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
