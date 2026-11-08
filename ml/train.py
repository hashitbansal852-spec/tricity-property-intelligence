import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

df = pd.read_csv("data/processed/cleaned_housing.csv")

X = df.drop(columns=["listing_id", "price_lakh"])
y = df["price_lakh"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

text_cols = ["city", "sector", "property_type", "furnishing"]

encode = ColumnTransformer(
    [("onehot", OneHotEncoder(handle_unknown="ignore"), text_cols)],
    remainder="passthrough",
)

linear = make_pipeline(encode, LinearRegression())

forest = make_pipeline(
    encode, RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)
)

linear.fit(X_train, y_train)
forest.fit(X_train, y_train)

param_grid = {
    "randomforestregressor__n_estimators": [100, 200, 300, 500],
    "randomforestregressor__max_depth": [10, 15, 20, None],
    "randomforestregressor__min_samples_split": [2, 5, 10],
    "randomforestregressor__min_samples_leaf": [1, 2, 4],
}

random_search = RandomizedSearchCV(
    estimator=forest,
    param_distributions=param_grid,
    n_iter=10,
    cv=5,
    scoring="neg_mean_absolute_error",
    random_state=42,
    n_jobs=-1,
    verbose=2,
)

random_search.fit(X_train, y_train)

print("\nBest Parameters:", random_search.best_params_)
print("Best CV MAE:", round(-random_search.best_score_, 2))

best_model = random_search.best_estimator_

linear_pred = linear.predict(X_test)
forest_pred = forest.predict(X_test)
tuned_pred = best_model.predict(X_test)

print(
    "\nTrained on",
    len(X_train),
    "homes. Testing on",
    len(X_test),
    "homes it has never seen.",
)


def evaluate_model(name, actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)
    r2 = r2_score(actual, predicted)

    print(f"\n{name}")
    print("MAE:", round(mae, 2))
    print("MSE:", round(mse, 2))
    print("RMSE:", round(rmse, 2))
    print("R2 Score:", round(r2, 4))


evaluate_model("Linear Regression", y_test, linear_pred)
evaluate_model("Original Random Forest", y_test, forest_pred)
evaluate_model("Tuned Random Forest", y_test, tuned_pred)

if mean_absolute_error(y_test, tuned_pred) < mean_absolute_error(y_test, forest_pred):
    best_model = best_model
    print("\nSelected Model: Tuned Random Forest")
else:
    best_model = forest
    print("\nSelected Model: Original Random Forest")

final_model = forest

joblib.dump(final_model, "models/property_model.pkl")

print("Model saved successfully!")