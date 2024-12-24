document.addEventListener('DOMContentLoaded', function(){
    // Получаем форму по ID
    const form = document.getElementById('search-form');
    // Получаем элемент сетки продуктов по ID
    const productGrid = document.getElementById('product-grid');
    // Получаем кнопку сброса по классу
    const resetButton = document.querySelector('.cancel-button');

    // Обработчик события отправки формы
    form.addEventListener('submit', function(event){
        event.preventDefault(); // Отменяем стандартное поведение формы
        makeAjaxRequest(); // Выполняем AJAX-запрос
    });

    // Обработчик события клика на кнопку сброса
    resetButton.addEventListener('click', function(event){
        event.preventDefault(); // Отменяем стандартное поведение кнопки
        form.reset(); // Сбрасываем форму
        makeAjaxRequest(); // Выполняем AJAX-запрос после сброса формы
    })

    // Функция для выполнения AJAX-запроса
    function makeAjaxRequest(){
        // Создаем объект FormData из формы
        const formData = new FormData(form);
        // Преобразуем данные формы в строку запроса
        const queryString = new URLSearchParams(formData).toString();

        // Выполняем AJAX-запрос
        fetch(`${window.location.pathname}?${queryString}`, {
            method:'GET', // Метод запроса GET
            headers:{
                'X-Requested-With':'XMLHttpRequest' // Заголовок для обозначения AJAX-запроса
            }
        })

        // Обрабатываем ответ в формате JSON
        .then(response => response.json())

        // Обрабатываем данные из ответа
        .then(data => {
            // Очищаем содержимое элемента сетки продуктов
            productGrid.innerHTML = '';

            // Проходим по каждому продукту из данных
            data.products.forEach(product => {
                // Создаем новый элемент для карточки продукта
                const productDiv = document.createElement('div');
                productDiv.classList.add('card'); // Добавляем класс для стилизации

                // Устанавливаем HTML-контент для карточки продукта
                productDiv.innerHTML = `
                <a href="product/${product.id}" class="card-link">
                    <div class="img-div">
                        <img src="static/images/${product.product_image}" alt="${product.product_name}" class="card-img">
                    </div>
                </a>
                <div class="card-body">
                    <a href="product/${product.id}" class="card-link">
                        <h5 class="card-title">
                            <p class="card-link">${product.product_name}</p>
                        </h5>
                        <p class="card-text">
                            <strong>Bahasy:</strong> <span style="color:#6236f4">${product.price} TMT</span><br>
                            <strong>Beyany:</strong> ${product.description}<br>
                        </p>
                    </a>
                </div>
                `;
                // Добавляем карточку продукта в элемент сетки продуктов
                productGrid.appendChild(productDiv);
            });
            
        })

        // Обрабатываем ошибки, если они произошли
        .catch(error => console.error('Error:', error));
    };

});
