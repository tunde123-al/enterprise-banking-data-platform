"""FastAPI event generator."""
import time
from datetime import UTC, datetime

from .generator_utils import RNG


def generate(account_ids, count=100, seed=20260817):
    """Generate a batch of account event records."""
    rng = __import__("random").Random(seed)
    return [{
        "event_id": rng.randint(100000, 999999),
        "account_id": rng.choice(account_ids),
        "amount": round(rng.uniform(1, 5000), 2),
        "event_type": rng.choice(['withdrawal', 'deposit', 'transfer', 'payment']),
        "timestamp": datetime.now(UTC).isoformat(),
        "status": "processed"
    } for _ in range(count)]


def generate_fastapi_event(account_ids):
    """Yield a single event dict."""
    return generate(account_ids, count=1, seed=RNG.randint(1, 10_000))[0]


def event_stream(account_ids):
    """Infinite generator of events."""
    while True:
        yield generate_fastapi_event(account_ids)
        time.sleep(RNG.uniform(0.1, 2.0))