import numpy as np
import pandas as pd


def build_chandigarh_dataset(n=2500, seed=43):

    rng = np.random.default_rng(seed)

    L = [
        ("Chandigarh", "Sector 8", 0, 22000, 27000, 2.5, 16, 2),
        ("Chandigarh", "Sector 9", 0, 23000, 28000, 2.0, 16, 2),
        ("Chandigarh", "Sector 10", 0, 21000, 26000, 2.5, 17, 2),
        ("Chandigarh", "Sector 16", 0, 20000, 24000, 1.5, 15, 2),
        ("Chandigarh", "Sector 21", 0, 17000, 22000, 1.5, 13, 3),
        ("Chandigarh", "Sector 27", 0, 16500, 21000, 3.0, 12, 3),
        ("Chandigarh", "Sector 35", 0, 15500, 20000, 2.5, 11, 3),
        ("Chandigarh", "Sector 33", 13500, 14500, 16000, 4.0, 9, 4),
        ("Chandigarh", "Sector 44", 13000, 14000, 15000, 5.0, 9, 4),
        ("Chandigarh", "Sector 46", 12500, 13500, 14500, 6.0, 8, 4),
        ("Chandigarh", "Sector 49", 14000, 0, 0, 7.0, 7, 5),
        ("Chandigarh", "Sector 51", 14500, 0, 0, 8.0, 7, 4),
        ("Chandigarh", "Sector 63", 12000, 0, 0, 9.0, 6, 4),
        ("Chandigarh", "Manimajra", 10500, 11000, 13000, 7.0, 15, 5),
        ("Panchkula", "Panchkula Sector 9", 13000, 15000, 20000, 9.0, 20, 3),
        ("Panchkula", "Panchkula Sector 20", 8500, 9000, 0, 12.0, 18, 4),
        ("Panchkula", "Panchkula Extension", 6500, 6800, 8500, 16.0, 22, 3),
        ("Mohali", "Mohali Sector 70", 11000, 11500, 14500, 10.0, 9, 4),
        ("Mohali", "Mohali Sector 82", 10400, 9500, 0, 14.0, 7, 4),
        ("Mohali", "Mohali Sector 88", 9600, 0, 0, 16.0, 9, 3),
        ("Mohali", "Aerocity", 8800, 8500, 10000, 15.0, 4, 4),
        ("Mohali", "Mohali Sector 118", 9500, 0, 0, 18.0, 12, 3),
        ("Zirakpur", "Zirakpur VIP Road", 6000, 5500, 0, 11.0, 6, 5),
        ("Zirakpur", "Zirakpur Patiala Road", 5200, 5000, 0, 12.0, 8, 4),
        ("Kharar", "Kharar Sunny Enclave", 4800, 4600, 5500, 18.0, 16, 4),
        ("Kharar", "Kharar Landran Road", 5300, 0, 0, 17.0, 14, 3),
        ("New Chandigarh", "New Chandigarh (Mullanpur)", 8000, 7500, 9000, 14.0, 25, 4),
    ]

    loc = pd.DataFrame(
        L,
        columns=["city", "sector", "f_rate", "b_rate", "i_rate", "c_dis", "a_dis", "w"],
    )

    idx = rng.choice(len(loc), size=n, p=loc.w / loc.w.sum())

    rows = []

    for i in idx:

        r = loc.iloc[i]
        types = []

        for t, rate in [
            ("Flat", r.f_rate),
            ("Builder Floor", r.b_rate),
            ("Independent House", r.i_rate),
        ]:
            if rate > 0:
                types.append(t)

        tw = {"Flat": 0.55, "Builder Floor": 0.30, "Independent House": 0.15}

        p = np.array([tw[t] for t in types])
        p = p / p.sum()
        ptype = rng.choice(types, p=p)

        if ptype == "Flat":
            bhk = rng.choice([1, 2, 3, 4], p=[0.10, 0.40, 0.40, 0.10])
            area = {1: (500, 750), 2: (850, 1250), 3: (1250, 1900), 4: (1900, 2800)}[
                bhk
            ]
            rate = r.f_rate

        elif ptype == "Builder Floor":
            bhk = rng.choice([2, 3, 4], p=[0.30, 0.50, 0.20])
            area = {2: (900, 1300), 3: (1300, 2000), 4: (2000, 2800)}[bhk]
            rate = r.b_rate

        else:
            bhk = rng.choice([3, 4, 5, 6], p=[0.25, 0.40, 0.27, 0.08])
            area = {
                3: (1800, 2800),
                4: (2800, 4500),
                5: (4500, 7000),
                6: (7000, 10000),
            }[bhk]
            rate = r.i_rate

        area_sqt = int(round(rng.uniform(*area), -1))

        bathrooms = np.clip(bhk + rng.choice([1, 0, 0, -1]), 1, bhk + 1)

        age = np.clip(rng.gamma(2.0, 5.0), 0, 40)

        if r.city in ("New Chandigarh", "Kharar", "Zirakpur") or r.sector in (
            "Aerocity",
            "Mohali Sector 118",
        ):
            age = np.clip(age * 0.4, 0, 15)

        furnishing = rng.choice(
            ["Unfurnished", "Semi-Furnished", "Fully Furnished"], p=[0.45, 0.40, 0.15]
        )

        parking = int(rng.choice([0, 1, 2], p=[0.15, 0.55, 0.30]))

        if ptype == "Flat":
            total_floors = rng.choice([4, 8, 12, 14, 18, 20])
            floor = rng.integers(0, total_floors)

        else:
            total_floors = 3 if ptype == "Independent House" else rng.choice([3, 4])
            floor = 0 if ptype == "Independent House" else rng.integers(0, total_floors)

        gated_prob = {
            "Flat": 0.80,
            "Builder Floor": 0.25,
            "Independent House": 0.15,
        }

        gated = int(rng.random() < gated_prob[ptype])
        park_facing = int(rng.random() < 0.25)
        corner = int(rng.random() < 0.20)

        dist_c = round(max(0.5, r.c_dis + rng.normal(0, 0.6)), 1)
        dist_a = round(max(1.0, r.a_dis + rng.normal(0, 0.8)), 1)

        dep = 0.004 if ptype == "Independent House" else 0.009
        m = max(0.72, 1 - dep * age)

        m *= {"Unfurnished": 1.00, "Semi-Furnished": 1.03, "Fully Furnished": 1.07}[
            furnishing
        ]
        m *= {0: 0.97, 1: 1.00, 2: 1.03}[parking]
        m *= 1.04 if gated else 1.0
        m *= 1.05 if park_facing else 1.0
        m *= 1.08 if corner else 1.0
        m *= max(0.94, 1 - 0.003 * dist_c)
        m *= max(0.97, 1 - 0.001 * dist_a)
        m *= 1 + 0.015 * max(0, bathrooms - bhk)

        if ptype == "Flat":
            m *= 0.97 if floor == total_floors - 1 else (1 + 0.004 * min(floor, 10))

        m *= rng.lognormal(0, 0.10)

        price_lakh = round(area_sqt * rate * m / 1e5, 1)

        rows.append(
            [
                r.city,
                r.sector,
                ptype,
                bhk,
                area_sqt,
                bathrooms,
                floor,
                total_floors,
                age,
                furnishing,
                parking,
                gated,
                park_facing,
                corner,
                dist_c,
                dist_a,
                price_lakh,
            ]
        )

    columns = [
        "city",
        "sector",
        "property_type",
        "bhk",
        "area_sqft",
        "bathrooms",
        "floor",
        "total_floors",
        "age_years",
        "furnishing",
        "parking",
        "gated_society",
        "park_facing",
        "corner_plot",
        "dist_city_centre_km",
        "dist_airport_km",
        "price_lakh",
    ]

    df = pd.DataFrame(rows, columns=columns)

    df[["age_years", "bathrooms"]] = df[["age_years", "bathrooms"]].astype(float)
    for col, frac in [("age_years", 0.03), ("bathrooms", 0.02), ("furnishing", 0.02)]:
        df.loc[rng.choice(n, int(n * frac), replace=False), col] = np.nan
    bad = rng.choice(n, 6, replace=False)
    df.loc[bad[:3], "price_lakh"] = df.loc[bad[:3], "price_lakh"] * 1e5
    df.loc[bad[3:], "area_sqft"] = 0
    dupes = df.sample(20, random_state=seed)
    df = pd.concat([df, dupes]).sample(frac=1, random_state=seed).reset_index(drop=True)
    df.insert(0, "listing_id", [f"CHD-{100001 + i}" for i in range(len(df))])
    return df

if __name__ == "__main__":
    df = build_chandigarh_dataset(n=2500, seed=43)

    df.to_csv("data/raw/chandigarh_housing.csv", index=False)

