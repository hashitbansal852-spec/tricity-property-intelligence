import sys
import json
import joblib
import pandas as pd
from pathlib import Path
import base64

MODEL_PATH = Path(__file__).resolve().parent / "models" / "property_model.pkl"

FEATURES = [
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
]


def predict_property(property_data):

    missing = [col for col in FEATURES if col not in property_data]

    if missing:
        raise ValueError(f"Missing features: {missing}")

    input_df = pd.DataFrame([property_data], columns=FEATURES)

    model = joblib.load(MODEL_PATH)

    prediction = model.predict(input_df)[0]

    return {
        "success": True,
        "predicted_price_lakh": round(float(prediction), 2),
        "predicted_price_crore": round(float(prediction / 100), 2),
    }


if __name__ == "__main__":

    try:

        if len(sys.argv) < 2:
            raise ValueError("Property data not provided")

        encoded_data = sys.argv[1]

        decoded_data = base64.b64decode(encoded_data).decode("utf-8")

        property_data = json.loads(decoded_data)

        if not isinstance(property_data, dict):
            raise ValueError("Input must be a JSON object")

        result = predict_property(property_data)

        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
