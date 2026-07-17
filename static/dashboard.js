console.log("QORESTO Dashboard Loaded");

// =============================
// COMMON CHART SETTINGS
// =============================

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,

    plugins: {
        legend: {
            labels: {
                color: "#ffffff"
            }
        }
    },

    scales: {
        x: {
            ticks: {
                color: "#ffffff"
            },
            grid: {
                color: "rgba(255,255,255,0.08)"
            }
        },

        y: {
            beginAtZero: true,
            ticks: {
                color: "#ffffff"
            },
            grid: {
                color: "rgba(255,255,255,0.08)"
            }
        }
    }
};

// =============================
// CUISINE BAR CHART
// =============================

if (document.getElementById("cuisineChart")) {

    new Chart(document.getElementById("cuisineChart"), {

        type: "bar",

        data: {
            labels: labels,
            datasets: [{
                label: "Restaurants",
                data: values,
                backgroundColor: "#4ddfff",
                borderRadius: 8
            }]
        },

        options: chartOptions
    });
}

// =============================
// CUISINE PIE CHART
// =============================

if (document.getElementById("pieChart")) {

    new Chart(document.getElementById("pieChart"), {

        type: "pie",

        data: {
            labels: labels,
            datasets: [{
                data: values,

                backgroundColor: [
                    "#4ddfff",
                    "#00e5ff",
                    "#00c3ff",
                    "#26c6da",
                    "#00acc1",
                    "#80deea"
                ]
            }]
        }
    });
}

// =============================
// MONTHLY REVENUE
// =============================

if (document.getElementById("revenueChart")) {

    new Chart(document.getElementById("revenueChart"), {

        type: "line",

        data: {
            labels: months,

            datasets: [{
                label: "Revenue",
                data: revenues,

                borderColor: "#4ddfff",
                backgroundColor: "rgba(77,223,255,0.2)",

                fill: true,
                tension: 0.4
            }]
        },

        options: chartOptions
    });
}

// =============================
// TOP ITEMS
// =============================

if (document.getElementById("topItemsChart")) {

    new Chart(document.getElementById("topItemsChart"), {

        type: "bar",

        data: {
            labels: itemLabels,

            datasets: [{
                label: "Quantity Sold",
                data: itemValues,
                backgroundColor: "#00e676",
                borderRadius: 8
            }]
        },

        options: chartOptions
    });
}

// =============================
// ORDER STATUS
// =============================

if (document.getElementById("statusChart")) {

    new Chart(document.getElementById("statusChart"), {

        type: "doughnut",

        data: {
            labels: statusLabels,

            datasets: [{
                data: statusValues,

                backgroundColor: [
                    "#4ddfff",
                    "#00e676",
                    "#ffd54f",
                    "#ff5252"
                ]
            }]
        }
    });
}

// =============================
// TOP RESTAURANTS
// =============================

if (document.getElementById("restaurantChart")) {

    new Chart(document.getElementById("restaurantChart"), {

        type: "bar",

        data: {
            labels: restaurantLabels,

            datasets: [{
                label: "Orders",
                data: restaurantValues,
                backgroundColor: "#2196f3",
                borderRadius: 8
            }]
        },

        options: chartOptions
    });
}

// =============================
// TOP CUSTOMERS
// =============================

if (document.getElementById("customerChart")) {

    new Chart(document.getElementById("customerChart"), {

        type: "bar",

        data: {
            labels: customerLabels,

            datasets: [{
                label: "Orders",
                data: customerValues,
                backgroundColor: "#ffd54f",
                borderRadius: 8
            }]
        },

        options: chartOptions
    });
}

// =============================
// PAYMENT STATUS
// =============================

if (document.getElementById("paymentChart")) {

    new Chart(document.getElementById("paymentChart"), {

        type: "pie",

        data: {
            labels: paymentLabels,

            datasets: [{
                data: paymentValues,

                backgroundColor: [
                    "#00e676",
                    "#4ddfff",
                    "#ff5252",
                    "#ffd54f"
                ]
            }]
        }
    });
}

console.log("All Charts Rendered Successfully");