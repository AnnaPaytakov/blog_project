document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll("#like-btn");

    likeButtons.forEach(button => {
        button.addEventListener("click", function () {
            const postId = this.getAttribute("data-id");
            const likeIcon = this.querySelector("#like-icon");
            const likeCount = this.closest(".like-button")?.querySelector(".like-count");

            fetch("/toggle-like/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: `post_id=${postId}`
            })
                .then(response => response.json())
                .then(data => {
                    if (data.liked) {
                        likeIcon.classList.add("filled");
                    } else {
                        likeIcon.classList.remove("filled");
                    }

                    if (likeCount) {
                        likeCount.textContent = data.likes_count;
                    }
                })
                .catch(error => console.error("Error:", error));
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}