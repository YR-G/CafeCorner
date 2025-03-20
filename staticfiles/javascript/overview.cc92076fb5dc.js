function initMap() {
    let mapDiv = document.getElementById("map");
    if (!mapDiv) return;

    let postcode = mapDiv.getAttribute("data-postcode");
    if (!postcode) {
        console.error("No postcode found");
        return;
    }
    let geocoder = new google.maps.Geocoder();
    let map = new google.maps.Map(mapDiv, {
        zoom: 15, // Default zoom level
        center: { lat: 51.5074, lng: -0.1278 } // Default center (London)
    });

    // Convert postcode to latitude and longitude
    geocoder.geocode({ address: postcode }, function(results, status) {
        if (status === "OK") {
            let location = results[0].geometry.location;
            map.setCenter(location);
            new google.maps.Marker({
                map: map,
                position: location,
                title: "Cafe Location"
            });
        } else {
            console.error("Geocode failed: " + status);
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    let reviewButton = document.getElementById("write-review-btn");
    if (reviewButton) {
        reviewButton.addEventListener("click", function() {
            let isLoggedIn = this.getAttribute("data-login") === "true"; // Check if the user is logged in
            let reviewUrl = this.getAttribute("data-url"); // Get review page URL

            if (isLoggedIn) {
                window.location.href = reviewUrl;
            } else {
                let loginUrl = "/users/login/?next=" + encodeURIComponent(reviewUrl);
                window.location.href = loginUrl;
            }
        });
    }
});
