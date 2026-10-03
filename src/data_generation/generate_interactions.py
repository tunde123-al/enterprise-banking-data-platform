from .core import DEFAULT_COUNTS, event_id, rng, timestamp, write_jsonl


def generate(customers, count=DEFAULT_COUNTS["interactions"], seed=20260817):
    r = rng(seed, 8)
    customer_ids = customers["customer_id"].tolist() if hasattr(customers, "__getitem__") else [row["customer_id"] for row in customers]
    return [{"interaction_id": event_id(), "customer_id": r.choice(customer_ids), "timestamp": timestamp(r), "channel": r.choice(("MOBILE_APP", "WEB", "CALL_CENTRE", "BRANCH")), "event": r.choice(("LOGIN", "PROFILE_UPDATE", "COMPLAINT", "PRODUCT_ENQUIRY"))} for _ in range(count)]
