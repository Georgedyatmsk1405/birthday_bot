```javascript
// Анимация появления элементов
function animateElements() {
    const elements = document.querySelectorAll('h1, table');
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 200 * index);
    });
}

// Запуск анимации при загрузке страницы
window.addEventListener('load', animateElements);

// Обработчик для прокрутки на мобильных устройствах
document.addEventListener('DOMContentLoaded', (event) => {
    const main = document.querySelector('main');
    let isScrolling;

    main.addEventListener('scroll', function () {
        window.clearTimeout(isScrolling);
        isScrolling = setTimeout(function () {
            console.log('Scrolling has stopped.');
        }, 66);
    }, false);
});

// Пример функции для получения списка кастомных уведомлений
fetch('/api/custom_notifications', {
    method: 'GET',
    headers: {"Authorization": window.Telegram.WebApp.initData},
}).then(response => {
    if (!response.ok) {
        console.log(response.status)
        throw new Error(`Network error: ${response.status}`);
    }
    return response.json();
}).then(data => {
    console.log(data);  // Здесь можно обработать полученные уведомления
}).catch(error => {
    console.error('An error occurred:', error);
    alert('Failed to load data. Please try again later.');
});
```
