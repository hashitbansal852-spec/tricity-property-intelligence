const compareForm = document.getElementById("compareForm");
const compareError = document.getElementById("compareError");
const comparisonResult = document.getElementById("comparisonResult");
const propertyAResult = document.getElementById("propertyAResult");
const propertyBResult = document.getElementById("propertyBResult");
const priceDifference = document.getElementById("priceDifference");

compareForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    compareError.textContent = "";
    comparisonResult.hidden = true;

    const a = document.getElementById("propertyA").value;
    const b = document.getElementById("propertyB").value;

    if (a === b) {
        compareError.textContent = "Please select two different properties.";
        return;
    }

    const button = compareForm.querySelector("button");

    try {
        button.disabled = true;
        button.textContent = "Comparing...";

        const response = await fetch("/api/compare", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ a, b })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Comparison failed");
        }

        const propertyA = data.propertyA;
        const propertyB = data.propertyB;

        function displayProperty(property) {
            return `
                <p><strong>ID:</strong> #${property.id}</p>
                <p><strong>City:</strong> ${property.city}</p>
                <p><strong>Sector:</strong> ${property.sector}</p>
                <p><strong>Type:</strong> ${property.property_type}</p>
                <p><strong>BHK:</strong> ${property.bhk}</p>
                <p><strong>Area:</strong> ${property.area_sqft} sqft</p>
                <p><strong>Bathrooms:</strong> ${property.bathrooms}</p>
                <p><strong>Furnishing:</strong> ${property.furnishing}</p>
                <p><strong>Predicted Price:</strong> ₹${Number(property.predicted_price_lakh).toFixed(2)} L</p>
            `;
        }

        propertyAResult.innerHTML = displayProperty(propertyA);
        propertyBResult.innerHTML = displayProperty(propertyB);

        priceDifference.textContent =
            `₹${Number(data.price_difference_lakh).toFixed(2)} L`;

        comparisonResult.hidden = false;

        comparisonResult.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (err) {
        compareError.textContent = err.message;

    } finally {
        button.disabled = false;
        button.textContent = "Compare Properties";
    }
});