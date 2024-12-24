const passwordField = document.getElementById('password'); 
// Получаем элемент с паролем по его ID 'password'

const togglePassword = document.getElementById('togglePassword'); 
// Получаем элемент чекбокса по его ID 'togglePassword'

togglePassword.addEventListener('change', function() { 
    // Добавляем обработчик события 'change' для чекбокса

    const currentType = passwordField.getAttribute('type'); 
    // Получаем текущее значение атрибута 'type' у поля пароля

    if (currentType === 'password') { 
        // Если текущее значение атрибута 'type' равно 'password'

        passwordField.setAttribute('type', 'text'); 
        // Меняем атрибут 'type' на 'text', чтобы сделать пароль видимым

    } else { 
        // В противном случае (если текущее значение 'type' не 'password')

        passwordField.setAttribute('type', 'password'); 
        // Меняем атрибут 'type' обратно на 'password', чтобы скрыть пароль
    }
});
