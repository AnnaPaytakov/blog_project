const passwordField1 = document.getElementById('id_password1'); 
const passwordField2 = document.getElementById('id_password2'); 
// Получаем элемент с паролем по его ID 'id_password'

const togglePassword = document.getElementById('togglePassword'); 
// Получаем элемент чекбокса по его ID 'togglePassword'

togglePassword.addEventListener('change', function() { 
    // Добавляем обработчик события 'change' для чекбокса

    const currentType = passwordField1.getAttribute('type'); 
    // Получаем текущее значение атрибута 'type' у поля пароля

    if (currentType === 'password') { 
        // Если текущее значение атрибута 'type' равно 'password'

        passwordField1.setAttribute('type', 'text'); 
        passwordField2.setAttribute('type', 'text'); 
        // Меняем атрибут 'type' на 'text', чтобы сделать пароль видимым

    } else { 
        // В противном случае (если текущее значение 'type' не 'password')

        passwordField1.setAttribute('type', 'password'); 
        passwordField2.setAttribute('type', 'password'); 
        // Меняем атрибут 'type' обратно на 'password', чтобы скрыть пароль
    }
});
