document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.getElementById("submit-review");
    const reviewForm = document.getElementById("review-form");

    submitButton.addEventListener("click", function (event) {
        event.preventDefault();

        let rating = document.querySelector(".rating-dropdown").value;
        let comment = document.getElementById("comment").value.trim();

        if (rating === "0") {
            alert("Please select a rating before submitting.");
            return;
        }
        if (comment === "") {
            alert("Please enter a comment before submitting.");
            return;
        }

        let confirmSubmit = confirm("Are you sure you want to submit your review?");
        if (confirmSubmit) {
            reviewForm.submit();
        }
    });
});
