const map = L.map("map").setView([30.7333, 76.7794], 11);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

async function loadLocalities() {
    try {
        const response = await fetch("/api/localities");

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || "Failed to load localities");
        }

        data.localities.forEach(locality => {

            L.marker([locality.lat, locality.lng])
                .addTo(map)
                .bindPopup(`<b>${locality.name}</b>`);

        });

        console.log(`${data.count} localities loaded successfully`);

    } catch (error) {
        console.error("Map Error:", error.message);
    }
}

loadLocalities();