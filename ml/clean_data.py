import pandas as pd

df = pd.read_csv(r"data/raw/chandigarh_housing.csv")

before = len(df)

dupes = df.duplicated(subset=df.columns.drop("listing_id"))

df = df[~dupes]
df = df[(df["area_sqft"] > 0) & (df["price_lakh"] <= 10000)]
df["bathrooms"] = df["bathrooms"].fillna(df["bhk"])
df["furnishing"] = df["furnishing"].fillna("Unfurnished")
df["age_years"] = df["age_years"].fillna(df["age_years"].mean())
df = df.reset_index(drop=True)

df.to_csv("data/processed/cleaned_housing.csv", index=False)