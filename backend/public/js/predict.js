const city = document.querySelector("#city");
const sector = document.querySelector("#sector");
const form = document.querySelector("#question-form");
const sub_btn = document.querySelector("#sub_btn");

const resultBox = document.querySelector("#prediction-result");
const errorMessage = document.querySelector("#error-message");

const areas = {
    "Chandigarh": [
        "Sector 8", "Sector 9", "Sector 10",
        "Sector 16", "Sector 21", "Sector 27",
        "Sector 35", "Sector 33", "Sector 44",
        "Sector 46", "Sector 49", "Sector 51",
        "Sector 63", "Manimajra"
    ],

    "Panchkula": [
        "Panchkula Sector 9",
        "Panchkula Sector 20",
        "Panchkula Extension"
    ],

    "Mohali": [
        "Mohali Sector 70",
        "Mohali Sector 82",
        "Mohali Sector 88",
        "Aerocity",
        "Mohali Sector 118"
    ],

    "Kharar": [
        "Kharar Sunny Enclave",
        "Kharar Landran Road"
    ],

    "Zirakpur": [
        "Zirakpur VIP Road",
        "Zirakpur Patiala Road"
    ],

    "New Chandigarh": [
        "New Chandigarh (Mullanpur)"
    ]
};

city.addEventListener("change", function () {

    sector.innerHTML = '<option value="">Select Area</option>';

    const selectedCity = city.value;

    if (areas[selectedCity]) {

        areas[selectedCity].forEach(function (area) {

            const option = document.createElement("option");

            option.value = area;
            option.textContent = area;

            sector.appendChild(option);

        });

    }

});

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    sub_btn.disabled = true;

    resultBox.style.display = "none";
    errorMessage.textContent = "";

    try {

        const propertyData = Object.fromEntries(
            new FormData(form).entries()
        );

        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(propertyData)
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(result.error || "Prediction failed");
        }

        document.querySelector("#predicted-price").textContent =
            `Estimated Price: ₹${result.predicted_price_lakh} Lakh`;

        document.querySelector("#predicted-crore").textContent =
            `₹${result.predicted_price_crore} Crore`;

        resultBox.style.display = "block";

    }

    catch (error) {

        console.error("Prediction error:", error);

        errorMessage.textContent =
            error.message || "Unable to connect to the server";

    }

    finally {

        sub_btn.disabled = false;

    }

});