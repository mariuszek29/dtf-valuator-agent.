#!/usr/bin/env python3
"""
DTF Valuator — Bittensor subnet fair-value screener
Author: YOUR NAME  License: MIT
"""

import requests, math, pandas as pd, time
from tabulate import tabulate

TAO_PRICE = 720  # update if you like

def fetch_subnets():
    url = "https://api.taostats.io/v2/subnets"
    return requests.get(url, timeout=30).json()

def discounted_tao_flow(apy, years=6, discount=0.25):
    flows = [(apy/100)/2**(n//2) for n in range(years)]
    return sum(f/(1+discount)**n for n, f in enumerate(flows))

def analyse():
    rows = []
    for s in fetch_subnets():
        apy = s["apy"]
        price = float(s["alpha_price_tao"])
        dcf = discounted_tao_flow(apy)
        fair_price = dcf * TAO_PRICE
        premium = price / fair_price
        rows.append(dict(
            id=s["uid"],
            symbol=s["symbol"],
            apy=apy,
            price=round(price,4),
            fair=round(fair_price,2),
            premium=round(premium,2)
        ))
    df = pd.DataFrame(rows).sort_values("premium")
    print(tabulate(df, headers="keys", tablefmt="github"))
    df.to_csv("valuation.csv", index=False)

if __name__ == "__main__":
    analyse()
