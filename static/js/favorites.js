document.addEventListener('DOMContentLoaded', function() {  
    const favoriteBtn = document.getElementById('favorite-btn');  
    const heartIcon = document.getElementById('heart-icon');  
    const favoriteText = document.getElementById('favorite-text'); // Добавляем текст для изменения

    favoriteBtn.addEventListener('click', function() {  
        const blogId = this.getAttribute('data-id');  

        fetch(`/add_to_favorites/${blogId}/`, {  
            method: 'POST',
            headers: {  
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'  
            }
        })
        .then(response => response.json())  
        .then(data => {  
            if (data.added) {  
                heartIcon.classList.add('filled');  
                favoriteText.textContent = 'Saved'; // Меняем текст на 'Saved'
            } else {  
                heartIcon.classList.remove('filled');  
                favoriteText.textContent = 'Save to favorites'; // Меняем текст обратно
            }
        })
        .catch(error => console.error('Error:', error));  
    });

    function getCookie(name) {  
        let cookieValue = null;  
        if (document.cookie && document.cookie !== '') {  
            const cookies = document.cookie.split(';');  
            for (let i = 0; i < cookies.length; i++) {  
                const cookie = cookies[i].trim();  
                if (cookie.substring(0, name.length + 1) === (name + '=')) {  
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));  
                    break;  
                }
            }
        }
        return cookieValue;  
    }
});
