// Добавляем обработчик события клика на элемент с id 'menu-toggle'
document.getElementById('menu-toggle').addEventListener('click', function() {
    // Находим элемент сайдбара по id 'sidebar'
    var sidebarEl = document.getElementById('sidebar');
    // Получаем текущий стиль элемента
    var sidebar = window.getComputedStyle(sidebarEl).left;
    // Проверяем, находится ли сайдбар вне экрана (слева от -250px)
    if (sidebar === '-250px') {
        // Если да, то перемещаем сайдбар на экран (слева 0px)
        sidebarEl.style.left = '0';
    } else {
        // Иначе, скрываем сайдбар, перемещая его за пределы экрана (слева -250px)
        sidebarEl.style.left = '-250px';
    }
});

// Добавляем обработчик события клика на элемент с id 'sidebar-close'
document.getElementById('sidebar-close').addEventListener('click', function() {
    // Находим элемент сайдбара по id 'sidebar' и скрываем его, перемещая за пределы экрана (слева -250px)
    document.getElementById('sidebar').style.left = '-250px';
});

