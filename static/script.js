// =============================
// LOAD ALL RESTAURANTS
// =============================

function loadRestaurants() {

    const container = document.getElementById("restaurants");

    if (!container) return;

    fetch('/restaurants')
        .then(response => response.json())
        .then(data => {
            displayRestaurants(data);
        })
        .catch(error => {
            console.error("Error loading restaurants:", error);
        });
}


// =============================
// DISPLAY RESTAURANTS
// =============================

function displayRestaurants(restaurants) {

    const container =
        document.getElementById("restaurants");

    if (!container) return;

    container.innerHTML = "";

    restaurants.forEach(restaurant => {

        const status =
            restaurant.status || "Open";

        const statusBadge =
            status === "Open"
                ? `<span class="status-open">🟢 Open</span>`
                : `<span class="status-closed">🔴 Closed</span>`;

        container.innerHTML += `

        <div class="restaurant-card">

            <img
                src="${restaurant.image_url || '/static/default.jpg'}"
                alt="${restaurant.restaurant_name}"
                class="restaurant-image"
            >

            <div class="card-content">

                <h2>${restaurant.restaurant_name}</h2>

                <p>📍 ${restaurant.city}</p>

                <p>🍽️ ${restaurant.cuisine}</p>

                <p>⭐ ${restaurant.rating}</p>

                <p>₹${restaurant.cost_for_two} for two</p>

                <p>${statusBadge}</p>

                <div class="card-buttons">

                    <a href="/menu/${restaurant.restaurant_id}">
                        <button>View Menu</button>
                    </a>

                    <a href="/restaurant/${restaurant.restaurant_id}">
                        <button>View Details</button>
                    </a>

                    <a href="/reviews/${restaurant.restaurant_id}">
                        <button>Reviews</button>
                    </a>

                    <a href="/add_favorite/${restaurant.restaurant_id}">
                        <button>❤️ Favorite</button>
                    </a>

                </div>

            </div>

        </div>
        `;

    });

}


// =============================
// SEARCH RESTAURANTS
// =============================

function searchRestaurant() {

    const searchInput =
        document.getElementById("searchInput");

    if (!searchInput) return;

    const keyword =
        searchInput.value.toLowerCase();

    fetch('/restaurants')
        .then(response => response.json())
        .then(data => {

            const filtered =
                data.filter(restaurant =>

                    restaurant.restaurant_name
                        .toLowerCase()
                        .includes(keyword)

                );

            displayRestaurants(filtered);

        })
        .catch(error => {
            console.error(error);
        });

}


// =============================
// CITY FILTER
// =============================

function filterByCity() {

    const city =
        document.getElementById("cityFilter").value;

    fetch('/restaurants')
        .then(response => response.json())
        .then(data => {

            if (city === "all") {
                displayRestaurants(data);
                return;
            }

            const filtered =
                data.filter(restaurant =>
                    restaurant.city === city
                );

            displayRestaurants(filtered);

        })
        .catch(error => {
            console.error(error);
        });

}


// =============================
// CUISINE FILTER
// =============================

function filterByCuisine() {

    const cuisine =
        document.getElementById("cuisineFilter").value;

    fetch('/restaurants')
        .then(response => response.json())
        .then(data => {

            if (
                cuisine === "All" ||
                cuisine === ""
            ) {
                displayRestaurants(data);
                return;
            }

            const filtered =
                data.filter(restaurant =>
                    restaurant.cuisine === cuisine
                );

            displayRestaurants(filtered);

        })
        .catch(error => {
            console.error(error);
        });

}


// =============================
// PAGE LOAD
// =============================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadRestaurants();

        const cityFilter =
            document.getElementById("cityFilter");

        if (cityFilter) {
            cityFilter.addEventListener(
                "change",
                filterByCity
            );
        }

        const cuisineFilter =
            document.getElementById("cuisineFilter");

        if (cuisineFilter) {
            cuisineFilter.addEventListener(
                "change",
                filterByCuisine
            );
        }

    }
);
function searchOrders() {

    let input =
    document.getElementById("searchInput")
    .value.toLowerCase();

    let rows =
    document.querySelectorAll("table tr");

    rows.forEach((row,index)=>{

        if(index===0) return;

        row.style.display =
        row.innerText.toLowerCase()
        .includes(input)
        ? ""
        : "none";

    });

}
// ==========================
// SCROLL REVEAL ANIMATION
// ==========================

function revealElements() {

    const reveals =
        document.querySelectorAll(
            '.feature-card, .stat-card, .restaurant-card'
        );

    reveals.forEach(item => {

        const windowHeight =
            window.innerHeight;

        const revealTop =
            item.getBoundingClientRect().top;

        if(revealTop < windowHeight - 100){

            item.classList.add("active");

        }

    });

}

window.addEventListener(
    "scroll",
    revealElements
);


// ==========================
// COUNTER ANIMATION
// ==========================

function animateCounters(){

    const counters =
        document.querySelectorAll('.counter');

    counters.forEach(counter=>{

        const target =
            Number(counter.dataset.target);

        let current = 0;

        const increment =
            target / 100;

        const updateCounter = ()=>{

            if(current < target){

                current += increment;

                counter.innerText =
                    Math.ceil(current);

                requestAnimationFrame(
                    updateCounter
                );

            }else{

                counter.innerText =
                    target.toLocaleString();

            }

        };

        updateCounter();

    });

}


// ==========================
// CARD TILT EFFECT
// ==========================

function initCardTilt(){

    const cards =
        document.querySelectorAll(
            '.restaurant-card,.feature-card,.stat-card'
        );

    cards.forEach(card=>{

        card.addEventListener(
            "mousemove",
            e=>{

                const rect =
                    card.getBoundingClientRect();

                const x =
                    e.clientX - rect.left;

                const y =
                    e.clientY - rect.top;

                const rotateX =
                    ((y / rect.height)-0.5)*-12;

                const rotateY =
                    ((x / rect.width)-0.5)*12;

                card.style.transform =
                    `perspective(1000px)
                    rotateX(${rotateX}deg)
                    rotateY(${rotateY}deg)
                    translateY(-10px)`;

            }
        );

        card.addEventListener(
            "mouseleave",
            ()=>{

                card.style.transform =
                    "";

            }
        );

    });

}


// ==========================
// PAGE LOADER
// ==========================

window.addEventListener(
    "load",
    ()=>{

        document.body.classList.add(
            "loaded"
        );

    }
);


// ==========================
// DOM READY
// ==========================

document.addEventListener(
    "DOMContentLoaded",
    ()=>{

        loadRestaurants();

        revealElements();

        animateCounters();

        setTimeout(()=>{

            initCardTilt();

        },1000);

    }
);
// ==========================================
// QORESTO PROFESSIONAL SCRIPT
// ==========================================

let allRestaurants = [];

// ==========================================
// LOAD RESTAURANTS
// ==========================================

async function loadRestaurants() {

    const container = document.getElementById("restaurants");

    if (!container) return;

    container.innerHTML = `
        <div class="loading">
            <div class="loader"></div>
            <h3>Loading Restaurants...</h3>
        </div>
    `;

    try {

        const response = await fetch("/restaurants");

        const data = await response.json();

        allRestaurants = data;

        displayRestaurants(data);

    } catch (error) {

        console.error(error);

        container.innerHTML = `
            <div class="error-box">
                <h3>⚠ Unable to Load Restaurants</h3>
                <p>Please try again later.</p>
            </div>
        `;
    }
}

// ==========================================
// DISPLAY RESTAURANTS
// ==========================================

function displayRestaurants(restaurants) {

    const container =
        document.getElementById("restaurants");

    if (!container) return;

    container.innerHTML = "";

    if (restaurants.length === 0) {

        container.innerHTML = `
            <div class="empty-state">
                <h2>🍽 No Restaurants Found</h2>
                <p>Try another search keyword.</p>
            </div>
        `;

        return;
    }

    restaurants.forEach((restaurant, index) => {

        const status =
            restaurant.status || "Open";

        const statusClass =
            status === "Open"
                ? "status-open"
                : "status-closed";

        const card = document.createElement("div");

        card.className = "restaurant-card";

        card.style.animationDelay =
            `${index * 0.08}s`;

        card.innerHTML = `

        <div class="image-wrapper">

            <img
                src="${restaurant.image_url || '/static/default.jpg'}"
                alt="${restaurant.restaurant_name}"
                class="restaurant-image"
            >

        </div>

        <div class="card-content">

            <h2>${restaurant.restaurant_name}</h2>

            <div class="restaurant-info">

                <p>📍 ${restaurant.city}</p>

                <p>🍽 ${restaurant.cuisine}</p>

                <p>⭐ ${restaurant.rating}</p>

                <p>💰 ₹${restaurant.cost_for_two} for two</p>

                <p class="${statusClass}">
                    ${status === "Open"
                        ? "🟢 Open Now"
                        : "🔴 Closed"}
                </p>

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
                    <button class="btn-secondary">
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
        `;

        container.appendChild(card);

    });
}

// ==========================================
// LIVE SEARCH
// ==========================================

function searchRestaurant() {

    const searchInput =
        document.getElementById("searchInput");

    if (!searchInput) return;

    const keyword =
        searchInput.value.toLowerCase();

    const filtered =
        allRestaurants.filter(r =>

            r.restaurant_name
                .toLowerCase()
                .includes(keyword)

            ||

            r.city
                .toLowerCase()
                .includes(keyword)

            ||

            r.cuisine
                .toLowerCase()
                .includes(keyword)

        );

    displayRestaurants(filtered);
}

// ==========================================
// CITY FILTER
// ==========================================

function filterByCity() {

    const city =
        document.getElementById("cityFilter").value;

    if (city === "all") {

        displayRestaurants(allRestaurants);

        return;
    }

    const filtered =
        allRestaurants.filter(

            r => r.city === city

        );

    displayRestaurants(filtered);
}

// ==========================================
// CUISINE FILTER
// ==========================================

function filterByCuisine() {

    const cuisine =
        document.getElementById("cuisineFilter").value;

    if (
        cuisine === "All" ||
        cuisine === ""
    ) {

        displayRestaurants(allRestaurants);

        return;
    }

    const filtered =
        allRestaurants.filter(

            r => r.cuisine === cuisine

        );

    displayRestaurants(filtered);
}

// ==========================================
// SEARCH ORDERS
// ==========================================

function searchOrders() {

    const input =
        document.getElementById("searchInput")
        .value
        .toLowerCase();

    const rows =
        document.querySelectorAll("table tr");

    rows.forEach((row, index) => {

        if (index === 0) return;

        row.style.display =
            row.innerText
                .toLowerCase()
                .includes(input)

                ? ""

                : "none";
    });
}

// ==========================================
// PAGE LOAD
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadRestaurants();

        const search =
            document.getElementById("searchInput");

        if (search) {

            search.addEventListener(
                "keyup",
                searchRestaurant
            );
        }

        const city =
            document.getElementById("cityFilter");

        if (city) {

            city.addEventListener(
                "change",
                filterByCity
            );
        }

        const cuisine =
            document.getElementById("cuisineFilter");

        if (cuisine) {

            cuisine.addEventListener(
                "change",
                filterByCuisine
            );
        }
    }
);
// Orders Chart

new Chart(
document.getElementById("ordersChart"),
{
    type:"line",

    data:{
        labels:orderDates,

        datasets:[{
            label:"Orders",
            data:orderCounts,

            borderColor:"#38BDF8",

            backgroundColor:"rgba(56,189,248,.2)",

            fill:true,

            tension:.4
        }]
    }
}
);


// Revenue Chart

new Chart(
document.getElementById("revenueChart"),
{
    type:"bar",

    data:{
        labels:revenueDates,

        datasets:[{
            label:"Revenue",

            data:revenues,

            backgroundColor:"#38BDF8"
        }]
    }
}
);


// Status Chart

new Chart(
document.getElementById("statusChart"),
{
    type:"pie",

    data:{
        labels:statusLabels,

        datasets:[{
            data:statusValues,

            backgroundColor:[
                "#00d4ff",
                "#10B981",
                "#F59E0B",
                "#EF4444"
            ]
        }]
    }
}
);


// Rating Chart

new Chart(
document.getElementById("ratingChart"),
{
    type:"doughnut",

    data:{
        labels:ratingLabels,

        datasets:[{
            data:ratingValues,

            backgroundColor:[
                "#38BDF8",
                "#10B981",
                "#F59E0B",
                "#EF4444"
            ]
        }]
    }
}
);
<script>

document.querySelectorAll(
'.feature-card,.restaurant-card,.stat-card'
).forEach(card=>{

card.addEventListener('mousemove',e=>{

const rect=
card.getBoundingClientRect();

const x=
e.clientX-rect.left;

const y=
e.clientY-rect.top;

const rotateY=
((x/rect.width)-0.5)*20;

const rotateX=
((y/rect.height)-0.5)*-20;

card.style.transform=
`perspective(1000px)
rotateX(${rotateX}deg)
rotateY(${rotateY}deg)
translateY(-10px)`;

});

card.addEventListener('mouseleave',()=>{

card.style.transform='';

});

});

</script>
// =============================
// LOAD ALL RESTAURANTS
// =============================

function loadRestaurants() {

    const container = document.getElementById("restaurants");

    if (!container) return;

    fetch('/restaurants')
        .then(response => response.json())
        .then(data => {
            displayRestaurants(data);
        })
        .catch(error => {
            console.error("Error loading restaurants:", error);
        });
}


// =============================
// DISPLAY RESTAURANTS
// =============================

function displayRestaurants(restaurants) {

    const container =
        document.getElementById("restaurants");

    if (!container) return;

    container.innerHTML = "";

    restaurants.forEach(restaurant => {

        const status =
            restaurant.status || "Open";

        const statusBadge =
            status === "Open"
                ? `<span class="status-open">🟢 Open</span>`
                : `<span class="status-closed">🔴 Closed</span>`;

        container.innerHTML += `

        <div class="restaurant-card">

            <img
                src="${restaurant.image_url || '/static/default.jpg'}"
                alt="${restaurant.restaurant_name}"
                class="restaurant-image"
            >

            <div class="card-content">

                <h2>${restaurant.restaurant_name}</h2>

                <p>📍 ${restaurant.city}</p>

                <p>🍽️ ${restaurant.cuisine}</p>

                <p>⭐ ${restaurant.rating}</p>

                <p>₹${restaurant.cost_for_two} for two</p>

                <p>${statusBadge}</p>

                <div class="card-buttons">

                    <a href="/menu/${restaurant.restaurant_id}">
                        <button>View Menu</button>
                    </a>

                    <a href="/restaurant/${restaurant.restaurant_id}">
                        <button>View Details</button>
                    </a>

                    <a href="/reviews/${restaurant.restaurant_id}">
                        <button>Reviews</button>
                    </a>

                    <a href="/add_favorite/${restaurant.restaurant_id}">
                        <button>❤️ Favorite</button>
                    </a>

                </div>

            </div>

        </div>
        `;

    });

}


// =============================
// SEARCH RESTAURANTS
// =============================

function searchRestaurant() {

    const searchInput =
        document.getElementById("searchInput");

    if (!searchInput) return;

    const keyword =
        searchInput.value.toLowerCase();

    fetch('/restaurants')
        .then(response => response.json())
        .then(data => {

            const filtered =
                data.filter(restaurant =>

                    restaurant.restaurant_name
                        .toLowerCase()
                        .includes(keyword)

                );

            displayRestaurants(filtered);

        })
        .catch(error => {
            console.error(error);
        });

}


// =============================
// CITY FILTER
// =============================

function filterByCity() {

    const city =
        document.getElementById("cityFilter").value;

    fetch('/restaurants')
        .then(response => response.json())
        .then(data => {

            if (city === "all") {
                displayRestaurants(data);
                return;
            }

            const filtered =
                data.filter(restaurant =>
                    restaurant.city === city
                );

            displayRestaurants(filtered);

        })
        .catch(error => {
            console.error(error);
        });

}


// =============================
// CUISINE FILTER
// =============================

function filterByCuisine() {

    const cuisine =
        document.getElementById("cuisineFilter").value;

    fetch('/restaurants')
        .then(response => response.json())
        .then(data => {

            if (
                cuisine === "All" ||
                cuisine === ""
            ) {
                displayRestaurants(data);
                return;
            }

            const filtered =
                data.filter(restaurant =>
                    restaurant.cuisine === cuisine
                );

            displayRestaurants(filtered);

        })
        .catch(error => {
            console.error(error);
        });

}


// =============================
// PAGE LOAD
// =============================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadRestaurants();

        const cityFilter =
            document.getElementById("cityFilter");

        if (cityFilter) {
            cityFilter.addEventListener(
                "change",
                filterByCity
            );
        }

        const cuisineFilter =
            document.getElementById("cuisineFilter");

        if (cuisineFilter) {
            cuisineFilter.addEventListener(
                "change",
                filterByCuisine
            );
        }

    }
);
function searchOrders() {

    let input =
    document.getElementById("searchInput")
    .value.toLowerCase();

    let rows =
    document.querySelectorAll("table tr");

    rows.forEach((row,index)=>{

        if(index===0) return;

        row.style.display =
        row.innerText.toLowerCase()
        .includes(input)
        ? ""
        : "none";

    });

}
// ==========================
// SCROLL REVEAL ANIMATION
// ==========================

function revealElements() {

    const reveals =
        document.querySelectorAll(
            '.feature-card, .stat-card, .restaurant-card'
        );

    reveals.forEach(item => {

        const windowHeight =
            window.innerHeight;

        const revealTop =
            item.getBoundingClientRect().top;

        if(revealTop < windowHeight - 100){

            item.classList.add("active");

        }

    });

}

window.addEventListener(
    "scroll",
    revealElements
);


// ==========================
// COUNTER ANIMATION
// ==========================

function animateCounters(){

    const counters =
        document.querySelectorAll('.counter');

    counters.forEach(counter=>{

        const target =
            Number(counter.dataset.target);

        let current = 0;

        const increment =
            target / 100;

        const updateCounter = ()=>{

            if(current < target){

                current += increment;

                counter.innerText =
                    Math.ceil(current);

                requestAnimationFrame(
                    updateCounter
                );

            }else{

                counter.innerText =
                    target.toLocaleString();

            }

        };

        updateCounter();

    });

}


// ==========================
// CARD TILT EFFECT
// ==========================

function initCardTilt(){

    const cards =
        document.querySelectorAll(
            '.restaurant-card,.feature-card,.stat-card'
        );

    cards.forEach(card=>{

        card.addEventListener(
            "mousemove",
            e=>{

                const rect =
                    card.getBoundingClientRect();

                const x =
                    e.clientX - rect.left;

                const y =
                    e.clientY - rect.top;

                const rotateX =
                    ((y / rect.height)-0.5)*-12;

                const rotateY =
                    ((x / rect.width)-0.5)*12;

                card.style.transform =
                    `perspective(1000px)
                    rotateX(${rotateX}deg)
                    rotateY(${rotateY}deg)
                    translateY(-10px)`;

            }
        );

        card.addEventListener(
            "mouseleave",
            ()=>{

                card.style.transform =
                    "";

            }
        );

    });

}


// ==========================
// PAGE LOADER
// ==========================

window.addEventListener(
    "load",
    ()=>{

        document.body.classList.add(
            "loaded"
        );

    }
);


// ==========================
// DOM READY
// ==========================

document.addEventListener(
    "DOMContentLoaded",
    ()=>{

        loadRestaurants();

        revealElements();

        animateCounters();

        setTimeout(()=>{

            initCardTilt();

        },1000);

    }
);
// ==========================================
// QORESTO PROFESSIONAL SCRIPT
// ==========================================

let allRestaurants = [];

// ==========================================
// LOAD RESTAURANTS
// ==========================================

async function loadRestaurants() {

    const container = document.getElementById("restaurants");

    if (!container) return;

    container.innerHTML = `
        <div class="loading">
            <div class="loader"></div>
            <h3>Loading Restaurants...</h3>
        </div>
    `;

    try {

        const response = await fetch("/restaurants");

        const data = await response.json();

        allRestaurants = data;

        displayRestaurants(data);

    } catch (error) {

        console.error(error);

        container.innerHTML = `
            <div class="error-box">
                <h3>⚠ Unable to Load Restaurants</h3>
                <p>Please try again later.</p>
            </div>
        `;
    }
}

// ==========================================
// DISPLAY RESTAURANTS
// ==========================================

function displayRestaurants(restaurants) {

    const container =
        document.getElementById("restaurants");

    if (!container) return;

    container.innerHTML = "";

    if (restaurants.length === 0) {

        container.innerHTML = `
            <div class="empty-state">
                <h2>🍽 No Restaurants Found</h2>
                <p>Try another search keyword.</p>
            </div>
        `;

        return;
    }

    restaurants.forEach((restaurant, index) => {

        const status =
            restaurant.status || "Open";

        const statusClass =
            status === "Open"
                ? "status-open"
                : "status-closed";

        const card = document.createElement("div");

        card.className = "restaurant-card";

        card.style.animationDelay =
            `${index * 0.08}s`;

        card.innerHTML = `

        <div class="image-wrapper">

            <img
                src="${restaurant.image_url || '/static/default.jpg'}"
                alt="${restaurant.restaurant_name}"
                class="restaurant-image"
            >

        </div>

        <div class="card-content">

            <h2>${restaurant.restaurant_name}</h2>

            <div class="restaurant-info">

                <p>📍 ${restaurant.city}</p>

                <p>🍽 ${restaurant.cuisine}</p>

                <p>⭐ ${restaurant.rating}</p>

                <p>💰 ₹${restaurant.cost_for_two} for two</p>

                <p class="${statusClass}">
                    ${status === "Open"
                        ? "🟢 Open Now"
                        : "🔴 Closed"}
                </p>

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
                    <button class="btn-secondary">
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
        `;

        container.appendChild(card);

    });
}

// ==========================================
// LIVE SEARCH
// ==========================================

function searchRestaurant() {

    const searchInput =
        document.getElementById("searchInput");

    if (!searchInput) return;

    const keyword =
        searchInput.value.toLowerCase();

    const filtered =
        allRestaurants.filter(r =>

            r.restaurant_name
                .toLowerCase()
                .includes(keyword)

            ||

            r.city
                .toLowerCase()
                .includes(keyword)

            ||

            r.cuisine
                .toLowerCase()
                .includes(keyword)

        );

    displayRestaurants(filtered);
}

// ==========================================
// CITY FILTER
// ==========================================

function filterByCity() {

    const city =
        document.getElementById("cityFilter").value;

    if (city === "all") {

        displayRestaurants(allRestaurants);

        return;
    }

    const filtered =
        allRestaurants.filter(

            r => r.city === city

        );

    displayRestaurants(filtered);
}

// ==========================================
// CUISINE FILTER
// ==========================================

function filterByCuisine() {

    const cuisine =
        document.getElementById("cuisineFilter").value;

    if (
        cuisine === "All" ||
        cuisine === ""
    ) {

        displayRestaurants(allRestaurants);

        return;
    }

    const filtered =
        allRestaurants.filter(

            r => r.cuisine === cuisine

        );

    displayRestaurants(filtered);
}

// ==========================================
// SEARCH ORDERS
// ==========================================

function searchOrders() {

    const input =
        document.getElementById("searchInput")
        .value
        .toLowerCase();

    const rows =
        document.querySelectorAll("table tr");

    rows.forEach((row, index) => {

        if (index === 0) return;

        row.style.display =
            row.innerText
                .toLowerCase()
                .includes(input)

                ? ""

                : "none";
    });
}

// ==========================================
// PAGE LOAD
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadRestaurants();

        const search =
            document.getElementById("searchInput");

        if (search) {

            search.addEventListener(
                "keyup",
                searchRestaurant
            );
        }

        const city =
            document.getElementById("cityFilter");

        if (city) {

            city.addEventListener(
                "change",
                filterByCity
            );
        }

        const cuisine =
            document.getElementById("cuisineFilter");

        if (cuisine) {

            cuisine.addEventListener(
                "change",
                filterByCuisine
            );
        }
    }
);
// Orders Chart

new Chart(
document.getElementById("ordersChart"),
{
    type:"line",

    data:{
        labels:orderDates,

        datasets:[{
            label:"Orders",
            data:orderCounts,

            borderColor:"#38BDF8",

            backgroundColor:"rgba(56,189,248,.2)",

            fill:true,

            tension:.4
        }]
    }
}
);


// Revenue Chart

new Chart(
document.getElementById("revenueChart"),
{
    type:"bar",

    data:{
        labels:revenueDates,

        datasets:[{
            label:"Revenue",

            data:revenues,

            backgroundColor:"#38BDF8"
        }]
    }
}
);


// Status Chart

new Chart(
document.getElementById("statusChart"),
{
    type:"pie",

    data:{
        labels:statusLabels,

        datasets:[{
            data:statusValues,

            backgroundColor:[
                "#00d4ff",
                "#10B981",
                "#F59E0B",
                "#EF4444"
            ]
        }]
    }
}
);


// Rating Chart

new Chart(
document.getElementById("ratingChart"),
{
    type:"doughnut",

    data:{
        labels:ratingLabels,

        datasets:[{
            data:ratingValues,

            backgroundColor:[
                "#38BDF8",
                "#10B981",
                "#F59E0B",
                "#EF4444"
            ]
        }]
    }
}
);
<script>

document.querySelectorAll(
'.feature-card,.restaurant-card,.stat-card'
).forEach(card=>{

card.addEventListener('mousemove',e=>{

const rect=
card.getBoundingClientRect();

const x=
e.clientX-rect.left;

const y=
e.clientY-rect.top;

const rotateY=
((x/rect.width)-0.5)*20;

const rotateX=
((y/rect.height)-0.5)*-20;

card.style.transform=
`perspective(1000px)
rotateX(${rotateX}deg)
rotateY(${rotateY}deg)
translateY(-10px)`;

});

card.addEventListener('mouseleave',()=>{

card.style.transform='';

});

});

</script>