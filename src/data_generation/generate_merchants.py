import os

import pandas as pd
import yaml

from .generator_utils import RNG, fake, get_mcc_codes, set_seed


def generate_merchants(config: dict) -> pd.DataFrame:
    n = config['volumes']['merchants']
    mcc_dict = get_mcc_codes()
    mcc_codes = list(mcc_dict.keys())

    data = []
    for i in range(1, n+1):
        mcc = RNG.choice(mcc_codes)
        data.append({
            "merchant_id": i,
            "merchant_name": fake.company(),
            "merchant_code": f"MC{RNG.randint(100000, 999999)}",
            "category_code": mcc,
            "category_name": mcc_dict[mcc],
            "address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "country": "USA",
            "created_date": fake.date_between(start_date="-5y", end_date="today")
        })
    return pd.DataFrame(data)


if __name__ == "__main__":
    with open("generator_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    set_seed(config['project']['seed'])
    df = generate_merchants(config)
    os.makedirs(config['output']['postgres_dir'], exist_ok=True)
    df.to_parquet(f"{config['output']['postgres_dir']}/merchants.parquet", index=False)
    print(f"Generated {len(df)} merchants.")