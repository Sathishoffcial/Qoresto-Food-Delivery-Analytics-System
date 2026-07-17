function displayRestaurants(restaurants) {

    const container = document.getElementById("restaurants");

    if (!container) return;

    container.innerHTML = "";

    restaurants.forEach(restaurant => {

        const status = restaurant.status || "Open";

        const statusBadge =
            status === "Open"
            ? `<span class="status-open">🟢 Open</span>`
            : `<span class="status-closed">🔴 Closed</span>`;

        container.innerHTML += `

        <div class="restaurant-card">

            <div class="image-wrapper">
                <img
                    src="${restaurant.image_url || '/static/default.jpg'}"
                    alt="${restaurant.restaurant_name}"
                    class="restaurant-image">
            </div>

            <div class="card-content">

                <h2>${restaurant.restaurant_name}</h2>

                <div class="restaurant-info">

                    <p>📍 ${restaurant.city}</p>

                    <p>🍽️ ${restaurant.cuisine}</p>

                    <p>⭐ ${restaurant.rating} / 5</p>

                    <p>💰 ₹${restaurant.cost_for_two} for two</p>

                    <p>${statusBadge}</p>

                </div>

                <div class="card-buttons">

                    <a href="/menu/${restaurant.restaurant_id}">
                        <button class="btn-primary">
                            Menu
                        </button>
                    </a>

                    <a href="/restaurant/${restaurant.restaurant_id}">
                        <button class="btn-secondary">
                            Details
                        </button>
                    </a>

                    <a href="/reviews/${restaurant.restaurant_id}">
                        <button class="btn-primary">
                            Reviews
                        </button>
                    </a>

                    <a href="/add_favorite/${restaurant.restaurant_id}">
                        <button class="btn-favorite">
                            ❤️ Favorite
                        </button>
                    </a>

                </div>

            </div>

        </div>

        `;
    });
}