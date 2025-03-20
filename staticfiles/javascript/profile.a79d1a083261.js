document.addEventListener("DOMContentLoaded", function () {
    const confirmBtn = document.getElementById("confirm-btn");
    const cancelBtn = document.getElementById("cancel-btn");

    if (confirmBtn) {
        confirmBtn.addEventListener("click", function (event) {
            event.preventDefault();

            let formData = {
                first_name: document.getElementById("firstname").value,
                last_name: document.getElementById("lastname").value,
                password: document.getElementById("password").value
            };

            fetch("/users/profile/", {
                method: "POST",
                body: JSON.stringify(formData),
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    document.getElementById("userDropdown").innerText = "Hi, " + formData.first_name;

                    let modal = new bootstrap.Modal(document.getElementById("successModal"));
                    modal.show();

                    document.getElementById("successModal").addEventListener("hidden.bs.modal", function () {
                        location.reload();
                    });
                } else {
                    showCustomModal("Error", data.message);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                showCustomModal("Error", "Failed to update profile. Please try again.");
            });
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener("click", function () {
            window.location.href = "/"; // redirect to homepage
        });
    }
});

// CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showCustomModal(title, message) {
    let modalHtml = `
        <div class="modal fade" id="customModal" tabindex="-1" aria-labelledby="customModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="customModalLabel">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">${message}</div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal">OK</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML("beforeend", modalHtml);
    let modal = new bootstrap.Modal(document.getElementById("customModal"));
    modal.show();

    document.getElementById("customModal").addEventListener("hidden.bs.modal", function () {
        document.getElementById("customModal").remove();
    });
}
