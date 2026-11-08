# 🏙️ Tricity Property Intelligence

An ML-powered real estate intelligence platform designed to predict property prices and explore the real estate market across Chandigarh, Mohali, Panchkula and surrounding Tricity regions.

The project combines Machine Learning, Python, Node.js, Express.js and MySQL to provide property price predictions, prediction history, property comparisons and interactive geographical exploration.

> [!IMPORTANT]
> **Data Disclaimer:** This project is an educational and experimental application. The property dataset contains sample/synthetic data and is not a verified collection of actual property transactions or current market listings. Consequently, model predictions and displayed price estimates are illustrative only. They should not be treated as actual market valuations or used for financial, investment or purchasing decisions.

---

## 🚀 Features

### 🧠 Machine Learning-Based Price Prediction

- Predict property prices using a trained Machine Learning model.
- Uses property characteristics such as:
  - City and sector
  - Property type
  - BHK configuration
  - Area in square feet
  - Number of bathrooms
  - Floor and total floors
  - Property age
  - Furnishing status
  - Parking availability
  - Gated society
  - Park-facing and corner-plot features
  - Distance from city centre and airport

### 📊 Prediction History

- Automatically stores successful property predictions in MySQL.
- View previously generated predictions.
- Retrieve property information from the database.

### ⚖️ Property Comparison

- Compare two previously saved property predictions.
- View property characteristics side by side.
- Calculate the difference between predicted prices.

### 🗺️ Interactive Property Map

- Explore localities across the Tricity region.
- Interactive maps powered by Leaflet.js.
- OpenStreetMap integration.
- Locality markers with geographical coordinates.

### 💻 Web Interface

- EJS-based frontend.
- Responsive CSS styling.
- Interactive JavaScript functionality.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Frontend | HTML, CSS, JavaScript, EJS |
| Backend | Node.js, Express.js |
| Database | MySQL |
| Machine Learning | Python, Scikit-learn |
| Data Processing | Pandas, NumPy |
| Model Serialization | Joblib |
| Maps | Leaflet.js, OpenStreetMap |
| Version Control | Git, GitHub |

---

## 🏗️ Project Architecture

The application follows a client-server architecture with a separate Python-based Machine Learning component.

```text
                 FRONTEND
              HTML / CSS / EJS
                     |
                     v
                EXPRESS.JS
                     |
          +----------+----------+
          |          |          |
          v          v          v
        MySQL     Python ML    REST APIs
          |          |
          |          v
          |     Scikit-learn
          |     Trained Model
          |       (.pkl)
          |          |
          +----------+
                     |
                     v
                JSON Response
                     |
                     v
                  FRONTEND
```

### How Prediction Works

1. The user enters property details through the frontend.
2. Express.js receives and validates the input.
3. Node.js communicates with Python using `child_process.execFile()`.
4. Python loads the trained Scikit-learn model.
5. The model generates a predicted property price.
6. The prediction is returned to Express.js.
7. Express.js stores the successful prediction in MySQL.
8. The frontend displays the prediction.

---

## 📁 Project Structure

```text
tricity-property-intelligence/
│
├── backend/
│   ├── data/
│   │   ├── localities.json
│   │   └── stats.json
│   │
│   ├── public/
│   │   ├── css/
│   │   │   ├── comparison.css
│   │   │   ├── history.css
│   │   │   ├── map.css
│   │   │   ├── predict.css
│   │   │   └── style.css
│   │   │
│   │   └── js/
│   │       ├── compare.js
│   │       ├── map.js
│   │       └── predict.js
│   │
│   ├── views/
│   │   ├── 404.ejs
│   │   ├── comparison.ejs
│   │   ├── history.ejs
│   │   ├── home.ejs
│   │   ├── map.ejs
│   │   └── predict.ejs
│   │
│   ├── db.js
│   ├── server.js
│   └── package.json
│
├── ml/
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   │
│   ├── models/
│   │   └── property_model.pkl
│   │
│   ├── clean_data.py
│   ├── generate_data.py
│   ├── predict.py
│   ├── train.py
│   └── requirements.txt
│
├── .gitignore
├── package.json
└── package-lock.json
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hashitbansal852-spec/tricity-property-intelligence.git
```

Navigate into the project:

```bash
cd tricity-property-intelligence
```

### 2. Install Node.js Dependencies

Install root dependencies:

```bash
npm install
```

Install backend dependencies:

```bash
cd backend
npm install
```

### 3. Set Up Python Environment

Navigate to the ML directory:

```bash
cd ../ml
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside the `backend` directory.

Configure your MySQL connection:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=tricity_db
DB_PORT=3306
```

Never commit your `.env` file or expose database credentials.

### 5. Set Up MySQL

Create the database:

```sql
CREATE DATABASE tricity_db;
```

Create the predictions table:

```sql
USE tricity_db;

CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    property_type VARCHAR(100) NOT NULL,
    bhk INT NOT NULL,
    area_sqft INT NOT NULL,
    bathrooms INT NOT NULL,
    floor INT NOT NULL,
    total_floors INT NOT NULL,
    age_years DECIMAL(5,2),
    furnishing VARCHAR(50) NOT NULL,
    parking INT NOT NULL,
    gated_society BOOLEAN NOT NULL,
    park_facing BOOLEAN NOT NULL,
    corner_plot BOOLEAN NOT NULL,
    dist_city_centre_km DECIMAL(6,2),
    dist_airport_km DECIMAL(6,2),
    predicted_price_lakh DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Run the Application

Start the backend from its directory:

```bash
cd backend
npm start
```

Open the application in your browser using the port configured in your Express server.

---

## 🗺️ Geographical Coverage

The platform focuses on the Tricity region, including:

- Chandigarh
- Mohali
- Panchkula
- Zirakpur
- Kharar
- New Chandigarh

Locality coordinates are maintained in the backend JSON data file and displayed using Leaflet and OpenStreetMap.

**Note:** Map markers represent locality reference points, not exact property locations.

---

## ⚠️ Limitations

- The model is trained on sample/synthetic property data.
- Predictions may not reflect actual market prices.
- Locality coordinates are reference points and may be approximate.
- Model performance on real-world property data has not been established.
- The application is currently an experimental project, not a production-grade property valuation service.

---

## 🔮 Future Improvements

- Advanced property search and filtering.
- Locality-wise price analytics.
- Improved model accuracy and feature engineering.
- Training and evaluation using verified real-world property datasets.
- Interactive property price visualizations.
- More detailed geographical property insights.
- Deployment with a production-ready database and ML environment.

---

## 👨‍💻 Author

**Hashit Bansal**

B.Tech Computer Science Engineering Student

Interested in Machine Learning, Artificial Intelligence, Full Stack Development and Data Science.

---

## ⭐ Support

If you find this project interesting, consider giving the repository a star!

Built with curiosity, learning and continuous improvement.
