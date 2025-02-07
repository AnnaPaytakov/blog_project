document.querySelector('.selected-language').addEventListener('click', function () {
    const options = document.querySelector('.language-options');
    options.style.display = options.style.display === 'none' || !options.style.display ? 'block' : 'none';
});

document.querySelectorAll('.language-options li').forEach(option => {
    option.addEventListener('click', function () {
        const selected = document.querySelector('.selected-language');
        selected.innerHTML = option.innerHTML;
        document.querySelector('.language-options').style.display = 'none';
        const value = option.getAttribute('data-value');
        console.log('Selected language:', value); // Replace with desired action
    });
});

document.addEventListener('click', function (e) {
    const selector = document.querySelector('.language-selector');
    if (!selector.contains(e.target)) {
        document.querySelector('.language-options').style.display = 'none';
    }
});