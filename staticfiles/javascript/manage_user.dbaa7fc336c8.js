// Update User Information
document.addEventListener("DOMContentLoaded", function () {
    const updateButtons = document.querySelectorAll(".update-btn");
    const updateForm = document.getElementById("updateUserForm");

    updateButtons.forEach(button => {
        button.addEventListener("click", function () {
            document.getElementById("update-user-id").value = this.dataset.id;
            document.getElementById("update-user-identity").value = this.dataset.identity;
            document.getElementById("update-user-firstname").value = this.dataset.firstname;
            document.getElementById("update-user-lastname").value = this.dataset.lastname;
            document.getElementById("update-user-email").value = this.dataset.email;
        });
    });

    updateForm.addEventListener("submit", function (event) {
        event.preventDefault();

        let formData = new FormData(updateForm);

        fetch(updateUserUrl, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "error") {
                showCustomModal("Error", data.message);
            } else {
                showCustomModal("Success", "User details updated successfully!", () => location.reload());
            }
        })
        .catch(error => console.error("Error:", error));
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            let userIdToDelete = this.dataset.id;
            let userName = this.dataset.name;

            showDeleteModal(userIdToDelete, userName);
        });
    });
});

function showDeleteModal(userId, userName) {
    let modalHtml = `
        <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="deleteModalLabel">Confirm Delete</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        Are you sure you want to delete <b>${userName}</b>?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-danger" id="confirmDeleteBtn" data-id="${userId}">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML("beforeend", modalHtml);
    let modal = new bootstrap.Modal(document.getElementById("deleteModal"));
    modal.show();

    document.getElementById("confirmDeleteBtn").addEventListener("click", function () {
        deleteUser(this.dataset.id);
    });

    document.getElementById("deleteModal").addEventListener("hidden.bs.modal", function () {
        document.getElementById("deleteModal").remove();
    });
}

// Delete User
function deleteUser(userId) {
    fetch(`/users/delete_user/${userId}/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            showCustomModal("Success", "User deleted successfully!", () => location.reload());
        } else {
            showCustomModal("Error", data.message);
        }
    })
    .catch(error => console.error("Error:", error));
}

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

