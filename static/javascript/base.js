document.addEventListener("DOMContentLoaded", function() {
    // Check if the user is authenticated
    const userAuthenticated = "{{ request.session.user_id|default:'' }}" !== "";

    // Prevent unauthorized users from accessing protected links
    document.querySelectorAll(".protected-link").forEach(link => {
        link.addEventListener("click", function(event) {
            if (!userAuthenticated) {
                event.preventDefault();
                // Redirect to login page with 'next' parameter
                const loginUrl = "/users/login/?next=" + encodeURIComponent(link.getAttribute("href"));
                window.location.href = loginUrl;
            }
        });
    });
});

// Handle search button click event
document.getElementById("search-button").addEventListener("click", function () {
    let query = document.getElementById("search-input").value.trim();

    // Show an alert if the input is empty
    if (query === "") {
        alert("Please enter a cafe name.");
        return;
    }

    // Send a request to search for the cafe
    fetch(`/search/?query=${query}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirect to the cafe overview page if found
                window.location.href = `/overview/${data.cafe_id}/`;
            } else {
                // Show a modal if no results are found
                let searchModal = new bootstrap.Modal(document.getElementById('searchModal'));
                searchModal.show();
            }
        })
        .catch(error => console.error("Error:", error));
});
