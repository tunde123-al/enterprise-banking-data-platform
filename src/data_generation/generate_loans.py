from datetime import datetime, timedelta

import pandas as pd

from .generator_utils import RNG, random_date, weighted_choice


def generate_loans(customers_df, accounts_df, config):
    n = config['volumes']['loans']
    loan_type_weights = config['distributions']['loan_type']
    customer_ids = customers_df['customer_id'].tolist()
    account_ids = accounts_df['account_id'].tolist()
    start_date = datetime.strptime(config['date_ranges']['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(config['date_ranges']['end_date'], "%Y-%m-%d").date()
    term_options = config['date_ranges']['loan_term_months']

    loans = []
    for i in range(1, n+1):
        ltype = weighted_choice(loan_type_weights)
        principal = round(RNG.uniform(1000, 500000), 2)
        term = RNG.choice(term_options)
        rate = round(RNG.uniform(0.025, 0.20), 4)
        orig = random_date(start_date, end_date)
        maturity = orig + timedelta(days=term*30)
        risk = RNG.choice(['A','B','C','D','E'])
        loans.append({
            "loan_id": i,
            "customer_id": RNG.choice(customer_ids),
            "account_id": RNG.choice(account_ids),
            "branch_id": RNG.randint(1, 5000),
            "loan_number": f"LN{RNG.randint(100000,999999)}",
            "loan_type": ltype,
            "principal_amount": principal,
            "interest_rate": rate,
            "current_balance": principal * RNG.uniform(0.3, 0.95),
            "term_months": term,
            "origination_date": orig,
            "maturity_date": maturity,
            "status": "active" if RNG.random() < 0.80 else "closed",
            "risk_rating": risk,
            "created_date": orig,
            "updated_date": orig
        })
    return pd.DataFrame(loans)