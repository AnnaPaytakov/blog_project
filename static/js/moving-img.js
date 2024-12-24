document.addEventListener("DOMContentLoaded", function() {
    // Ждем полной загрузки DOM, прежде чем запускать скрипт
    const image = document.getElementById("moving-image");  // Получаем элемент изображения по его ID
    let moveRight = true;  // Переменная для отслеживания направления движения (вправо)
    const speed = 0.5;  // Настройка скорости движения изображения
    let position = 0;  // Начальная позиция изображения
    const maxPosition = 50;  // Максимальная позиция для смещения изображения (50px)

    function animateImage() {
        if (moveRight) {  // Если движение вправо
            position += speed;  // Увеличиваем позицию на величину скорости
            if (position >= maxPosition) moveRight = false;  // Если достигли 50px, меняем направление на левое
        } else {  // Если движение влево
            position -= speed;  // Уменьшаем позицию на величину скорости
            if (position <= 0) moveRight = true;  // Если достигли начальной позиции, меняем направление на правое
        }

        image.style.left = position + "px";  // Применяем текущее смещение к стилю элемента (смещение по оси X)
        requestAnimationFrame(animateImage);  // Рекурсивно вызываем анимацию для плавного движения
    }

    animateImage();  // Запускаем анимацию
});

