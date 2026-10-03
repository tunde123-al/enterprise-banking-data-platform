"""
Generate synthetic customer records.
"""
import os
from datetime import datetime

import pandas as pd
import yaml

from .generator_utils import RNG, fake, generate_phone, hash_string, random_date, set_seed


def generate_customers(config: dict) -> pd.DataFrame:
    """Generate customer records."""
    n = config['volumes']['customers']
    start_date = datetime.strptime(config['date_ranges']['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(config['date_ranges']['end_date'], "%Y-%m-%d").date()

    data = {
        "customer_id": [],
        "first_name": [],
        "last_name": [],
        "email": [],
        "phone": [],
        "date_of_birth": [],
        "ssn_hash": [],
        "address": [],
        "city": [],
        "state": [],
        "zip": [],
        "country": [],
        "kyc_tier": [],
        "created_date": [],
        "updated_date": [],
        "is_active": []
    }

    for i in range(1, n+1):
        first = fake.first_name()
        last = fake.last_name()
        ssn = fake.ssn()
        ssn_hash = hash_string(ssn)
        dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
        city = fake.city()
        state = fake.state_abbr()
        zip_code = fake.zipcode()
        created = random_date(start_date, end_date)
        updated = random_date(created, end_date)

        data["customer_id"].append(i)
        data["first_name"].append(first)
        data["last_name"].append(last)
        data["email"].append(f"{first.lower()}.{last.lower()}@email.com")
        data["phone"].append(generate_phone())
        data["date_of_birth"].append(dob)
        data["ssn_hash"].append(ssn_hash)
        data["address"].append(fake.street_address())
        data["city"].append(city)
        data["state"].append(state)
        data["zip"].append(zip_code)
        data["country"].append("USA")
        data["kyc_tier"].append(RNG.choices(["TIER_1", "TIER_2", "TIER_3"], weights=[0.7, 0.2, 0.1], k=1)[0])
        data["created_date"].append(created)
        data["updated_date"].append(updated)
        data["is_active"].append(True if RNG.random() < 0.95 else False)

    return pd.DataFrame(data)


if __name__ == "__main__":
    with open("generator_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    set_seed(config['project']['seed'])
    df = generate_customers(config)
    os.makedirs(config['output']['postgres_dir'], exist_ok=True)
    df.to_parquet(f"{config['output']['postgres_dir']}/customers.parquet", index=False)
    oracle_df = df[['customer_id', 'first_name', 'last_name', 'ssn_hash', 'date_of_birth', 'address', 'city', 'state', 'zip', 'country']]
    oracle_df.columns = ['CUSTOMER_ID', 'FIRST_NAME', 'LAST_NAME', 'SSN_HASH', 'DOB', 'ADDRESS', 'CITY', 'STATE', 'ZIP', 'COUNTRY']
    os.makedirs(config['output']['oracle_dir'], exist_ok=True)
    oracle_df.to_parquet(f"{config['output']['oracle_dir']}/hist_customers.parquet", index=False)
    print(f"Generated {len(df)} customers.")