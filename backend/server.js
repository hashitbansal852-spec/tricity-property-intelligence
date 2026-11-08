require("dotenv").config()
const express = require("express")
const path = require("path")
const fs = require("fs")
const { execFile } = require("child_process")
const { promisify } = require("util")
const db = require("./db")


const runFile = promisify(execFile)

const app = express()
const port = process.env.PORT || 3000

const mlPath = path.join(__dirname, "..", "ml", "venv", "Scripts", "python.exe")
const predictPath = path.join(__dirname, "..", "ml", "predict.py")

app.set("view engine", "ejs")
app.set("views", path.join(__dirname, "views"))

app.use(express.static(path.join(__dirname, "public/css")))
app.use(express.static(path.join(__dirname, "public/js")))

app.use(express.urlencoded({ extended: true }))
app.use(express.json())

const json_helper = (filepath) => {
    try {
        return JSON.parse(fs.readFileSync(path.join(__dirname, filepath), "utf-8"))
    } catch (err) {
        console.error("Unable to read", filepath, err.message)
        return null
    }
}

app.get("/", (req, res) => {
    const stats = json_helper("data/stats.json")
    res.render("home", { stats })
})

app.get("/predict", (req, res) => {
    res.render("predict")
})

app.get("/compare", (req, res) => {
    res.status(200).render("comparison")
});

app.get("/map", (req, res) => {
    res.status(200).render("map")
})

app.get("/history", async (req, res) => {
    try {
        const [rows] = await db.execute(
            `SELECT * FROM predictions 
            ORDER BY created_at DESC 
            LIMIT 50`
        )

        res.render("history", { predictions: rows })

    } catch (err) {
        console.error("History error:", err.message);

        res.status(500).send("Unable to load prediction history");
    }
});

app.post("/api/predict", async (req, res) => {
    try {

        const {
            city, sector, property_type, bhk, area_sqft, bathrooms, floor,
            total_floors, age_years, furnishing, parking, gated_society,
            park_facing, corner_plot, dist_city_centre_km, dist_airport_km
        } = req.body;

        const propertyData = {
            city, sector, property_type, bhk, area_sqft, bathrooms, floor,
            total_floors, age_years, furnishing, parking, gated_society,
            park_facing, corner_plot, dist_city_centre_km, dist_airport_km
        };

        const missing = Object.entries(propertyData)
            .filter(([key, value]) =>
                value === undefined || value === null || value === ""
            )
            .map(([key]) => key);

        if (missing.length > 0) {
            return res.status(400).json({
                success: false,
                error: "Missing required features",
                missing
            });
        }

        const numericFeatures = [
            "bhk", "area_sqft", "bathrooms", "floor", "total_floors",
            "age_years", "parking", "gated_society", "park_facing",
            "corner_plot", "dist_city_centre_km", "dist_airport_km"
        ];

        for (const feature of numericFeatures) {
            propertyData[feature] = Number(propertyData[feature]);

            if (!Number.isFinite(propertyData[feature])) {
                return res.status(400).json({
                    success: false,
                    error: `Invalid value for ${feature}`
                });
            }
        }

        for (const feature of ["gated_society", "park_facing", "corner_plot"]) {
            if (![0, 1].includes(propertyData[feature])) {
                return res.status(400).json({
                    success: false,
                    error: `${feature} must be either 0 or 1`
                });
            }
        }

        const limits = {
            bhk: [1, 6],
            area_sqft: [200, 20000],
            bathrooms: [1, 8],
            floor: [0, 60],
            total_floors: [1, 60],
            age_years: [0, 60],
            parking: [0, 5],
            dist_city_centre_km: [0, 100],
            dist_airport_km: [0, 100]
        };

        for (const [feature, [min, max]] of Object.entries(limits)) {
            if (propertyData[feature] < min || propertyData[feature] > max) {
                return res.status(400).json({
                    success: false,
                    error: `${feature} must be between ${min} and ${max}`
                });
            }
        }

        if (propertyData.floor >= propertyData.total_floors) {
            return res.status(400).json({
                success: false,
                error: "floor must be lower than total_floors"
            });
        }

        const encodedData = Buffer
            .from(JSON.stringify(propertyData))
            .toString("base64");

        let output;

        try {
            const { stdout } = await runFile(mlPath, [
                predictPath,
                encodedData
            ]);

            output = JSON.parse(stdout);

        } catch (err) {
            console.error("predict.py failed:", err.message);

            try {
                const pyError = JSON.parse(err.stdout);

                return res.status(400).json({
                    success: false,
                    error: pyError.error
                });

            } catch {
                return res.status(500).json({
                    success: false,
                    error: "Unable to generate property prediction"
                });
            }
        }

        if (!output.success) {
            return res.status(500).json({
                success: false,
                error: output.error
            });
        }

        const [result] = await db.execute(
            `INSERT INTO predictions (
        city, sector, property_type, bhk, area_sqft, bathrooms,
        floor, total_floors, age_years, furnishing, parking,
        gated_society, park_facing, corner_plot,
        dist_city_centre_km, dist_airport_km, predicted_price_lakh
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
            [
                propertyData.city,
                propertyData.sector,
                propertyData.property_type,
                propertyData.bhk,
                propertyData.area_sqft,
                propertyData.bathrooms,
                propertyData.floor,
                propertyData.total_floors,
                propertyData.age_years,
                propertyData.furnishing,
                propertyData.parking,
                propertyData.gated_society,
                propertyData.park_facing,
                propertyData.corner_plot,
                propertyData.dist_city_centre_km,
                propertyData.dist_airport_km,
                output.predicted_price_lakh
            ]
        );

        return res.json({
            success: true,
            prediction_id: result.insertId,
            predicted_price_lakh: output.predicted_price_lakh,
            predicted_price_crore: output.predicted_price_crore
        });

    } catch (err) {
        console.error("Prediction error:", err);

        return res.status(500).json({
            success: false,
            error: "Unable to generate property prediction"
        });
    }
});

app.post("/api/compare", async (req, res) => {
    try {
        const { a, b } = req.body;

        if (!a || !b) {
            return res.status(400).json({
                success: false,
                error: "Both property IDs are required"
            });
        }

        const idA = Number(a);
        const idB = Number(b);

        if (
            !Number.isInteger(idA) ||
            !Number.isInteger(idB) ||
            idA <= 0 ||
            idB <= 0
        ) {
            return res.status(400).json({
                success: false,
                error: "Invalid property IDs"
            });
        }

        if (idA === idB) {
            return res.status(400).json({
                success: false,
                error: "Please select two different properties"
            });
        }

        const [rows] = await db.execute(
            `SELECT * FROM predictions
             WHERE id IN (?, ?)`,
            [idA, idB]
        );

        if (rows.length !== 2) {
            return res.status(404).json({
                success: false,
                error: "One or both predictions were not found"
            });
        }

        const propertyA = rows.find(row => row.id === idA);
        const propertyB = rows.find(row => row.id === idB);

        const priceDifference = Math.abs(
            Number(propertyA.predicted_price_lakh) -
            Number(propertyB.predicted_price_lakh)
        );

        return res.json({
            success: true,
            propertyA,
            propertyB,
            price_difference_lakh: Number(priceDifference.toFixed(2))
        });

    } catch (err) {
        console.error("Comparison error:", err.message);

        return res.status(500).json({
            success: false,
            error: "Unable to compare properties"
        });
    }
});

app.get("/api/localities", (req, res) => {
    try {
        const filePath = path.join(__dirname, "data", "localities.json");

        const fileData = fs.readFileSync(filePath, "utf-8");
        const localities = JSON.parse(fileData);

        res.json({
            success: true,
            count: localities.length,
            localities
        });

    } catch (error) {
        console.error("Localities API Error:", error.message);

        res.status(500).json({
            success: false,
            error: "Unable to fetch localities"
        });
    }
});

app.all("/*splat", (req, res) => {
    res.status(404).render("404")
})

app.use((err, req, res, next) => {
    console.error(err)
    res.status(500).json({ error: "Internal Server Error" })
})

app.listen(port, () => {
    console.log(`Server is live at ${port}`)
})