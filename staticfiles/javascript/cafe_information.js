document.getElementById("uploadTrigger").addEventListener("click", function(event) {
    event.preventDefault();
    document.getElementById("imageUpload").click();
});

document.getElementById("imageUpload").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById("imagePreview").src = e.target.result;
        };
        reader.readAsDataURL(file);

        uploadToCloudinary(file);
    }
});

//Cloudinary upload function
function uploadToCloudinary(file) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("upload_preset", "cafe_preset");

    fetch("https://api.cloudinary.com/v1_1/dfk7crlez/image/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.secure_url) {
            updateImageUrlInDatabase(data.secure_url); // ✅ 更新数据库
        } else {
            alert("Image upload failed!");
        }
    })
    .catch(error => console.error("Error uploading image:", error));
}

// Update the database
function updateImageUrlInDatabase(imageUrl) {
    fetch("cafes/update_cafe_image/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ img_url: imageUrl })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            document.getElementById("imagePreview").src = imageUrl;
            alert("Image updated successfully!");
        } else {
            alert("Error updating image.");
        }
    })
    .catch(error => console.error("Error updating image:", error));
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
