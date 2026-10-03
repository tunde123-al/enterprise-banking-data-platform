from .core import DEFAULT_COUNTS, rng, uid, write_csv


def generate(customers, count=DEFAULT_COUNTS["cards"], seed=20260817):
    r = rng(seed, 6)
    customer_ids = customers["customer_id"].tolist() if hasattr(customers, "__getitem__") else [row["customer_id"] for row in customers]
    return [{"card_id": uid("CRD", n), "customer_id": r.choice(customer_ids), "masked_pan": f"5399********{r.randrange(1000, 9999)}", "card_type": r.choice(("DEBIT", "CREDIT")), "status": r.choice(("ACTIVE", "BLOCKED", "EXPIRED"))} for n in range(1, count + 1)]
