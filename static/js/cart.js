document.addEventListener('DOMContentLoaded', function () {  
    // Код выполняется после полной загрузки DOM-структуры страницы.

    const addBtn = document.getElementById('add-btn');  
    // Получаем элемент кнопки для добавления товара в корзину.

    const subtractBtn = document.getElementById('subtract-btn');  
    // Получаем элемент кнопки для уменьшения количества товара в корзине.

    const cartQuantity = document.getElementById('cart-quantity');  
    // Получаем элемент, отображающий количество товара в корзине.

    const stockQuantity = parseInt('{{ product.stock_quantity }}');  
    // Получаем количество товара на складе из бэкенда.

    addBtn.addEventListener('click', function () {  
        // Добавляем слушатель события на кнопку "Добавить", который срабатывает при клике.

        const productId = addBtn.getAttribute('data-id');  
        // Получаем ID продукта из атрибута "data-id" кнопки.

        updateCart('add', productId);  
        // Вызываем функцию обновления корзины для добавления товара.
    });

    subtractBtn.addEventListener('click', function () {  
        // Добавляем слушатель события на кнопку "Уменьшить", который срабатывает при клике.

        const productId = subtractBtn.getAttribute('data-id');  
        // Получаем ID продукта из атрибута "data-id" кнопки.

        updateCart('subtract', productId);  
        // Вызываем функцию обновления корзины для уменьшения количества товара.
    });

    function updateCart(action, productId) {  
        // Функция для обновления количества товара в корзине (добавление или уменьшение).

        let url = action === 'add' ? '/add-to-cart/' : '/subtract-from-cart/';  
        // Выбираем правильный URL в зависимости от действия (добавить или уменьшить товар).

        fetch(url, {  
            // Отправляем запрос на сервер с использованием метода fetch.

            method: 'POST',  
            // Устанавливаем метод POST для отправки данных.

            headers: {  
                'X-CSRFToken': getCookie('csrftoken'),  
                // Передаем CSRF токен для защиты от подделки запросов.

                'Content-Type': 'application/json',  
                // Устанавливаем тип содержимого как JSON.
            },

            body: JSON.stringify({ product_id: productId }),  
            // Отправляем ID продукта в теле запроса в формате JSON.
        })
        .then(response => response.json())  
        // Ожидаем ответ от сервера и преобразуем его в JSON.

        .then(data => {  
            // Обрабатываем полученные данные.

            if (data.status === 'success') {  
                // Если статус ответа "успех".

                cartQuantity.textContent = data.quantity;  
                // Обновляем количество товара на странице.

                if (data.quantity >= stockQuantity) {  
                    // Если количество в корзине равно или больше, чем на складе.

                    addBtn.disabled = true;  
                    // Деактивируем кнопку "Добавить".

                    alert('Siz bu önümiň skladdaky mukdaryna ýetdiňiz.');  
                    // Выводим сообщение на туркменском языке: "Siz bu önümiň skladdaky mukdaryna ýetdiňiz."
                } else {  
                    // Если количество товара меньше, чем на складе.

                    addBtn.disabled = false;  
                    // Активируем кнопку "Добавить".
                }
            } else if (data.status === 'error') {  
                // Если статус ответа "ошибка".

                alert(data.message);  
                // Выводим сообщение с ошибкой.

                addBtn.disabled = true;  
                // Деактивируем кнопку "Добавить", если достигнут лимит на складе.
            }
        })
        .catch(error => console.error('Error:', error));  
        // Обрабатываем ошибки запроса и выводим их в консоль.
    }

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
