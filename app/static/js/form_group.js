document.getElementById('appointmentForm').addEventListener('submit', function (e) {

    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const notification_interval = document.getElementById('notification_interval').value.trim();

    const userId = document.getElementById('user_id').value;

    // Проверяем валидность полей
    if (name.length < 2 || name.length > 50) {
        alert("Имя должно быть от 2 до 50 символов.");
        return;
    }




    // Создаем объект с данными
    const appointmentData = {
        name: name,
        user_id: userId,
        notification_interval: notification_interval,
    };

    // Преобразуем объект в JSON строку
    const jsonData = JSON.stringify(appointmentData);
    fetch('/api/group', {
    method: 'post',
    headers: {"Authorization": window.Telegram.WebApp.initData},
    body: jsonData,
})
.then(response => {
    if (!response.ok) {
      console.log(response.status)
      console.log(response.status)
      throw new Error(`Ошибка сети: ${response.status}`);
    }
    const popupMessage = `Группа создана`;
    document.getElementById('popupMessage').textContent = popupMessage;

    document.getElementById('popup').style.display = 'flex';
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => {
    console.error('Произошла ошибка:', error);
    alert('Не удалось загрузить данные. Пожалуйста, попробуйте позже.');
  });

});

document.getElementById('closePopup').addEventListener('click', async function () {
    setTimeout(() => {
            window.Telegram.WebApp.close();
        }, 100);
});

// Анимация появления элементов при загрузке страницы
function animateElements() {
    const elements = document.querySelectorAll('h1, .form-group, .btn');
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 100 * index);
    });
}

// Стили для анимации
var styleSheet = document.styleSheets[0];
styleSheet.insertRule(`
    h1, .form-group, .btn {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.5s ease, transform 0.5s ease;
    }
`, styleSheet.cssRules.length);

// Плавное появление страницы при загрузке
window.addEventListener('load', function () {
    document.body.style.opacity = '1';
    animateElements();
});

styleSheet.insertRule(`
    body {
        opacity: 0;
        transition: opacity 0.5s ease;
`, styleSheet.cssRules.length);

