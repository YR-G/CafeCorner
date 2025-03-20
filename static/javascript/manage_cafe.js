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

// Update Cafe Shop Information
document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded!");
    const updateButtons = document.querySelectorAll(".update-btn");
    const updateForm = document.getElementById("updateCafeForm");
    updateButtons.forEach(button => {
        button.addEventListener("click", function () {
            document.getElementById("update-cafe-id").value = this.dataset.id;
            document.getElementById("update-cafe-name").value = this.dataset.name;
            document.getElementById("update-owner-name").value = this.dataset.owner;
            document.getElementById("update-address").value = this.dataset.address;
            document.getElementById("update-email").value = this.dataset.email;
            document.getElementById("update-price-range").value = this.dataset.price;
        });
    });

    updateForm.addEventListener("submit", function (event) {
        event.preventDefault();

        let formData = new FormData(updateForm);

        fetch(updateCafeUrl,{
            method: "POST",
            body: formData,
            headers: {
                            "X-CSRFToken": getCookie("csrftoken")
                        }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "error") {
                alert(data.message);
            } else {
                alert("Update successful!");
                location.reload();
            }
        })
        .catch(error => console.error("Error:", error));
    });
});

// Delete Cafe Shop Information
document.addEventListener("DOMContentLoaded", function () {
    let cafeIdToDelete;
    let cafeNameToDelete;

    const deleteButtons = document.querySelectorAll(".delete-btn");
    const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
    const deleteCafeNameSpan = document.getElementById("cafeNameToDelete");
    const deleteConfirmModal = document.getElementById("deleteConfirmModal");
    const cancelDeleteBtn = document.getElementById("cancelDeleteBtn");

    if (!confirmDeleteBtn || !deleteCafeNameSpan || !deleteConfirmModal || !cancelDeleteBtn) {
        console.error("One or more required elements are missing.");
        return;
    }

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            cafeIdToDelete = this.dataset.id;
            cafeNameToDelete = this.dataset.name;

            if (cafeIdToDelete && cafeNameToDelete) {
                deleteCafeNameSpan.textContent = cafeNameToDelete;
                deleteConfirmModal.style.display = "block";
            } else {
                console.error("Missing cafe ID or name.");
            }
        });
    });

    confirmDeleteBtn.addEventListener("click", function () {
        if (!cafeIdToDelete) {
            console.error("Cafe ID is missing.");
            return;
        }

        fetch(`/delete_cafe/${cafeIdToDelete}/`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text) });
            }
            return response.json();
        })
        .then(data => {
            if (data.status === "success") {
                showCustomModal("Success", "Café deleted successfully!", () => location.reload());
            } else {
                showCustomModal("Error", data.message);
            }
        })
        .catch(error => console.error("Error:", error));
    });

    cancelDeleteBtn.addEventListener("click", function () {
        deleteConfirmModal.style.display = "none";
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            document.cookie.split(";").forEach(cookie => {
                let trimmedCookie = cookie.trim();
                if (trimmedCookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(trimmedCookie.substring(name.length + 1));
                }
            });
        }
        return cookieValue;
    }
});


function showCustomModal(title, message, callback = null) {
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
        if (callback) callback();
    });
}

