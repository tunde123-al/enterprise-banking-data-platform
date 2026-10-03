from .core import DEFAULT_COUNTS, rng, uid, write_csv


def generate(customers, count=DEFAULT_COUNTS["devices"], seed=20260817):
    r = rng(seed, 9)
    customer_ids = customers["customer_id"].tolist() if hasattr(customers, "__getitem__") else [row["customer_id"] for row in customers]
    return [{"device_id": uid("DEV", n), "customer_id": r.choice(customer_ids), "platform": r.choice(("ANDROID", "IOS", "WEB")), "risk_score": round(r.random(), 3), "trusted": r.choice((True, False))} for n in range(1, count + 1)]
