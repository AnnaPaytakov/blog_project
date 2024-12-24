const phoneInput = document.getElementById('phone'); // Получаем элемент input по его ID 'phone'
const errorMessage = document.getElementById('error-message'); // Получаем элемент для отображения сообщения об ошибке по его ID 'error-message'
const countryCode = '+993'; // Устанавливаем код страны в переменной

// Функция для установки позиции курсора сразу после кода страны
function setCursorPositionAfterCountryCode() {
    const cursorPosition = countryCode.length + 1; // Вычисляем позицию курсора после кода страны (+1 для пробела)
    phoneInput.setSelectionRange(cursorPosition, cursorPosition); // Устанавливаем курсор на вычисленную позицию
}

// Функция для предотвращения удаления кода страны
function preventRemovingCountryCode(event) {
    if (event.key === 'Backspace') { // Проверяем, если была нажата клавиша Backspace
        const cursorPosition = phoneInput.selectionStart; // Получаем текущую позицию курсора
        if (cursorPosition <= countryCode.length) { // Если курсор находится до или на позиции кода страны
            event.preventDefault(); // Предотвращаем удаление кода страны
        }
    }
}

// Функция для проверки количества цифр после кода страны
function limitPhoneNumberLength(event) {
    const phoneNumber = phoneInput.value.replace(countryCode, '').trim(); // Убираем код страны и лишние пробелы из значения
    const digitCount = (phoneNumber.match(/\d/g) || []).length; // Считаем количество цифр в номере телефона

    if (digitCount >= 8 && /\d/.test(event.key)) { // Если цифр уже 8 или больше и введённая клавиша также является цифрой
        event.preventDefault(); // Предотвращаем ввод дополнительных цифр
    }
}

// Добавляем обработчик события при фокусе на поле ввода
phoneInput.addEventListener('focus', function () {
    if (phoneInput.value === '') { // Если поле ввода пустое
        phoneInput.value = countryCode + ' '; // Добавляем код страны и пробел в поле ввода
    }
    setCursorPositionAfterCountryCode(); // Устанавливаем курсор после кода страны
});

// Добавляем обработчик события при изменении значения в поле ввода
phoneInput.addEventListener('input', function (e) {
    let value = e.target.value.replace(/[^0-9+]/g, ''); // Удаляем все символы, кроме цифр и знака '+'
    if (!value.startsWith(countryCode)) { // Если значение не начинается с кода страны
        value = countryCode + ' ' + value.replace(countryCode, ''); // Добавляем код страны и пробел в начале
    }
    e.target.value = value; // Устанавливаем отформатированное значение обратно в поле ввода
});

// Добавляем обработчик для предотвращения удаления кода страны
phoneInput.addEventListener('keydown', preventRemovingCountryCode);

// Добавляем обработчик для ограничения количества цифр после кода страны
phoneInput.addEventListener('keydown', limitPhoneNumberLength);

// Функция для проверки корректности номера телефона
function validatePhoneNumber() {
    const phoneNumber = phoneInput.value.replace(countryCode, '').trim(); // Убираем код страны и лишние пробелы из значения
    const digitCount = (phoneNumber.match(/\d/g) || []).length; // Считаем количество цифр в номере телефона
    return digitCount >= 8; // Проверяем, что цифр не меньше 8
}

// Добавляем обработчик события при потере фокуса с поля ввода
phoneInput.addEventListener('blur', function () {
    if (!validatePhoneNumber()) { // Если номер телефона некорректный (меньше 8 цифр)
        errorMessage.style.display = 'block'; // Показываем сообщение об ошибке
    } else {
        errorMessage.style.display = 'none'; // Скрываем сообщение об ошибке
    }
});
