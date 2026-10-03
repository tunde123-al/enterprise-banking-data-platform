"""
Shared utilities for data generation.
Provides deterministic ID generation, date sampling, and weighted random selection.
"""
import random
import hashlib
import uuid
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()
RNG = random.Random(42)  # global seeded random

def set_seed(seed: int = 42) -> None:
    """Set seed for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    Faker.seed(seed)

def generate_id(prefix: str = "", length: int = 10) -> str:
    """Generate a unique ID with optional prefix."""
    return f"{prefix}{RNG.randint(10**(length-1), 10**length - 1)}"

def generate_uuid() -> str:
    """Generate a UUID v4 string."""
    return str(uuid.uuid4())

def hash_string(value: str, salt: str = "BANK_SALT_2026") -> str:
    """SHA-256 hash of a string with salt."""
    return hashlib.sha256(f"{salt}{value}".encode()).hexdigest()

def random_date(start: date, end: date) -> date:
    """Return a random date between start and end."""
    delta = (end - start).days
    return start + timedelta(days=RNG.randint(0, delta))

def random_timestamp(start: date, end: date) -> datetime:
    """Return a random datetime between start and end."""
    dt = random_date(start, end)
    hour = RNG.randint(0, 23)
    minute = RNG.randint(0, 59)
    second = RNG.randint(0, 59)
    return datetime(dt.year, dt.month, dt.day, hour, minute, second)

def weighted_choice(weights: Dict[Any, float]) -> Any:
    """Choose an item based on weights."""
    items = list(weights.keys())
    probs = list(weights.values())
    return RNG.choices(items, weights=probs, k=1)[0]

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(value, max_val))

def generate_balance(account_type: str) -> float:
    """Generate a realistic account balance based on account type."""
    if account_type == "checking":
        return round(RNG.uniform(100, 15000), 2)
    elif account_type == "savings":
        return round(RNG.uniform(500, 50000), 2)
    elif account_type == "money_market":
        return round(RNG.uniform(1000, 100000), 2)
    elif account_type == "cd":
        return round(RNG.uniform(5000, 200000), 2)
    elif account_type == "ira":
        return round(RNG.uniform(1000, 500000), 2)
    else:
        return round(RNG.uniform(100, 10000), 2)

def generate_transaction_amount(transaction_type: str) -> float:
    """Generate a transaction amount based on type."""
    if transaction_type in ["withdrawal", "payment"]:
        # most withdrawals are < $500
        return round(np.random.lognormal(mean=4.0, sigma=1.2), 2)
    elif transaction_type == "deposit":
        return round(np.random.lognormal(mean=5.0, sigma=1.5), 2)
    elif transaction_type == "transfer":
        return round(np.random.lognormal(mean=4.5, sigma=1.3), 2)
    else:  # fee
        return round(np.random.uniform(1, 50), 2)

def generate_phone() -> str:
    """Generate a US phone number."""
    return f"{RNG.randint(200,999)}-{RNG.randint(200,999)}-{RNG.randint(1000,9999)}"

def get_mcc_codes() -> Dict[str, str]:
    """Return a dict of MCC codes and descriptions."""
    # Partial list of real MCC codes
    return {
        "5411": "Grocery Stores, Supermarkets",
        "5812": "Eating Places, Restaurants",
        "5814": "Fast Food Restaurants",
        "5541": "Service Stations, Gas Stations",
        "5732": "Electronics Stores",
        "5311": "Department Stores",
        "5651": "Family Clothing Stores",
        "5691": "Men's and Women's Clothing Stores",
        "5941": "Sporting Goods Stores",
        "5942": "Book Stores",
        "5977": "Cosmetic Stores",
        "5999": "Miscellaneous and Specialty Retail",
        "7011": "Hotels, Motels, Resorts",
        "4112": "Railroads, Passenger",
        "4121": "Taxicabs, Limousines",
        "4131": "Bus Lines",
        "4214": "Motor Freight Carriers, Trucking",
        "4225": "Warehousing, Storage",
        "4511": "Airlines, Air Carriers",
        "4722": "Travel Agencies, Tour Operators",
        "4814": "Telecommunication Services",
        "4816": "Computer Network Services",
        "4899": "Cable, Satellite, Other Pay TV",
        "4900": "Utilities, Electric, Gas, Sanitary",
        "5912": "Drug Stores, Pharmacies",
        "5921": "Package Stores, Beer, Wine, Liquor",
        "5944": "Jewelry Stores",
        "5945": "Hobby, Toy, and Game Stores",
        "5946": "Camera and Photographic Supply Stores",
        "5947": "Gift, Card, Novelty, Souvenir Shops",
        "5948": "Luggage and Leather Goods Stores",
        "5949": "Sewing, Needlework, Fabric, Piece Goods",
        "5950": "Glass, Paint, Wallpaper Stores",
        "5960": "Direct Marketing - Insurance Services",
        "5961": "Direct Marketing - Catalog Merchants",
        "5962": "Direct Marketing - Mail Order",
        "5963": "Door-to-Door Sales",
        "5964": "Direct Marketing - Telemarketing",
        "5965": "Direct Marketing - Outbound Telemarketing",
        "5966": "Direct Marketing - Inbound Telemarketing",
        "5967": "Direct Marketing - Direct Mail",
        "5968": "Direct Marketing - Subscriptions",
        "5969": "Direct Marketing - Other",
        "5970": "Artist Supply Stores",
        "5971": "Art Dealers, Galleries",
        "5972": "Stamp and Coin Stores",
        "5973": "Religious Goods Stores",
        "5974": "Used Merchandise Stores",
        "5975": "Pawn Shops",
        "5976": "Miscellaneous and Specialty Retail",
        "5977": "Cosmetic Stores",
        "5978": "Typewriter Stores",
        "5983": "Fuel Oil Dealers",
        "5992": "Florists",
        "5993": "Cigar Stores and Stands",
        "5994": "News Dealers, Newsstands",
        "5995": "Pet Shops",
        "5996": "Swimming Pools, Sales and Service",
        "5997": "Electric Razor Stores",
        "5998": "Tent and Awning Shops",
        "5999": "Miscellaneous and Specialty Retail"
    }