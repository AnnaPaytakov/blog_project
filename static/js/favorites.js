document.addEventListener('DOMContentLoaded', function() {  
    // Ждем, пока вся страница полностью загрузится, перед выполнением кода
    const favoriteBtn = document.getElementById('favorite-btn');  
    // Получаем кнопку с id 'favorite-btn'
    const heartIcon = document.getElementById('heart-icon');  
    // Получаем иконку сердца с id 'heart-icon'

    favoriteBtn.addEventListener('click', function() {  
        // Добавляем обработчик событий для клика по кнопке "favoriteBtn"
        const productId = this.getAttribute('data-id');  
        // Получаем значение атрибута 'data-id', которое содержит id продукта

        fetch(`/add_to_favorites/${productId}/`, {  
            // Выполняем запрос на сервер по URL, передавая id продукта
            method: 'POST',  // Указываем метод POST для запроса
            headers: {  
                'X-CSRFToken': getCookie('csrftoken'),  
                // Передаем CSRF-токен для безопасности
                'Content-Type': 'application/json'  
                // Указываем, что данные будут в формате JSON
            }
        })
        .then(response => response.json())  
        // Ждем ответ от сервера и преобразуем его в JSON
        .then(data => {  
            // Обрабатываем полученные данные от сервера
            if (data.added) {  
                // Если продукт был добавлен в избранное
                heartIcon.classList.add('filled');  
                // Добавляем класс 'filled' к иконке сердца, чтобы изменить его внешний вид
            } else {  
                // Если продукт был удален из избранного
                heartIcon.classList.remove('filled');  
                // Убираем класс 'filled' у иконки сердца
            }
        })
        .catch(error => console.error('Error:', error));  
        // Если произошла ошибка, выводим ее в консоль
    });

    function getCookie(name) {  
        // Функция для получения значения определенной cookie по имени
        let cookieValue = null;  
        // Инициализируем переменную для хранения значения cookie
        if (document.cookie && document.cookie !== '') {  
            // Проверяем, существуют ли cookie в документе
            const cookies = document.cookie.split(';');  
            // Разбиваем строку cookie на массив отдельных cookie
            for (let i = 0; i < cookies.length; i++) {  
                // Перебираем каждую cookie
                const cookie = cookies[i].trim();  
                // Удаляем пробелы в начале и в конце строки cookie
                if (cookie.substring(0, name.length + 1) === (name + '=')) {  
                    // Проверяем, начинается ли текущая cookie с имени, которое мы ищем
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));  
                    // Если cookie найдена, декодируем её значение
                    break;  
                    // Останавливаем цикл после нахождения нужной cookie
                }
            }
        }
        return cookieValue;  
        // Возвращаем значение найденной cookie
    }
});
