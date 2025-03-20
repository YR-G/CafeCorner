document.addEventListener("DOMContentLoaded", function() {
    const filterSelect = document.getElementById("filter-options");
    const orderSelect = document.getElementById("sort-order");
    const cafeListContainer = document.getElementById("cafe-list");

    function fetchSortedCafes() {
        const filter = filterSelect.value;
        const order = orderSelect.value;

        fetch(`/sorting/?filter=${filter}&order=${order}`, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            cafeListContainer.innerHTML = "";

            if (data.length === 0) {
                cafeListContainer.innerHTML = `
                    <div class="no-cafes-message">
                        <h2>No cafes found.</h2>
                        <p>Please check back later!</p>
                    </div>`;
                return;
            }

            data.forEach(cafe => {
                const cafeHTML = `
                    <a href="/overview/${cafe.id}/" class="cafe-item-link">
                        <div class="cafe-item">
                            <img src="${cafe.img_url}" class="cafe-img" alt="${cafe.name}">
                            <div class="cafe-info">
                                <h2>${cafe.name}</h2>
                                <p class="rating"><strong>${cafe.average_rating}</strong></p>
                                <p><strong>Address:</strong> ${cafe.address}</p>
                                <p><strong>Average Price:</strong> ${cafe.price_range} per person</p>
                                <p><strong>Reviews:</strong> ${cafe.reviews_count}</p>
                                <p><strong>Introduction:</strong> ${cafe.description}</p>
                            </div>
                        </div>
                    </a>`;
                cafeListContainer.innerHTML += cafeHTML;
            });
        })
        .catch(error => console.error("Error fetching sorted cafes:", error));
    }

    filterSelect.addEventListener("change", fetchSortedCafes);
    orderSelect.addEventListener("change", fetchSortedCafes);
});
