from .core import DEFAULT_COUNTS, rng, timestamp, uid, write_csv


def generate(loans, count=DEFAULT_COUNTS["repayments"], seed=20260817):
    r = rng(seed, 5)
    loan_ids = loans["loan_id"].tolist() if hasattr(loans, "__getitem__") else [row["loan_id"] for row in loans]
    return [{"repayment_id": uid("REP", n), "loan_id": r.choice(loan_ids), "payment_ts": timestamp(r), "amount": round(r.uniform(10_000, 500_000), 2), "status": r.choice(("POSTED", "LATE", "FAILED"))} for n in range(1, count + 1)]
