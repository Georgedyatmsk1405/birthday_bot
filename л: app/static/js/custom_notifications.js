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

const urlParams = new URLSearchParams(window.location.search);
const group_id = urlParams.get('group_id');
const user_id = urlParams.get('user_id');

fetch(`/api/notification/${group_id}?user_id=${user_id}`, {
    method: 'get',
    headers: {"Authorization": window.Telegram.WebApp.initData},
})
.then(response => {
    if (!response.ok) {
      console.log(response.status)
      console.log(response.status)
      throw new Error(`Ошибка сети: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
  console.log(data)
  let div = document.createElement('div');
  if ("message" in data){
  div.className = "alert";
  div.innerHTML = "<strong>Нет уведомлений в данной группе </strong>";
  document.body.append(div);
  }
  if ("notifications" in data){
  innerHTML = '<div class="child y proximity-scroll-snapping" dir="rtl">'
  for (val of data.notifications) {
       text = `<table>
                 <tr>
                   <td>${val.content}</td>
                   <td><button onclick="deleteNotification(${val.id})">Удалить уведомление</button></td>
                 </tr>
               </table>`
       innerHTML+=text
  }
  innerHTML+='</div>'
  div.className = "alert";
  div.innerHTML = innerHTML;
  document.body.append(div);
  }

  })
  .catch(error => {
    console.error('Произошла ошибка:', error);
    alert('Не удалось загрузить данные. Пожалуйста, попробуйте позже.');
  });

function deleteNotification(notification_id) {
    fetch(`/api/notification/${notification_id}`, {
        method: 'DELETE',
        headers: {"Authorization": window.Telegram.WebApp.initData},
    })
    .then(response => {
        if (!response.ok) {
          console.log(response.status)
          console.log(response.status)
          throw new Error(`Ошибка сети: ${response.status}`);
        }
        location.reload(); // Перезагрузка страницы после удаления уведомления
    })
    .catch(error => {
        console.error('Произошла ошибка:', error);
        alert('Не удалось удалить уведомление. Попробуйте еще раз.');
    });
}

document.getElementById('appointmentForm').addEventListener('submit', function (e) {

    e.preventDefault();
    const content = document.getElementById('content').value.trim();

    const userId = document.getElementById('user_id').value;

    // Проверяем валидность поля
    if (content.length < 2 || content.length > 255) {
        alert("Текст уведомления должен быть от 2 до 255 символов.");
        return;
    }

    // Создаем объект с данными
    const appointmentData = {
        content: content,
        group_id: group_id,
        user_id: userId,
    };

    // Преобразуем объект в JSON строку
    const jsonData = JSON.stringify(appointmentData);
    fetch(`/api/notification/${group_id}`, {
    method: 'POST',
    headers: {"Authorization": window.Telegram.WebApp.initData},
    body: jsonData,
})
.then(response => {
    if (!response.ok) {
      console.log(response.status)
      console.log(response.status)
      throw new Error(`Ошибка сети: ${response.status}`);
    }
    const popupMessage = `Уведомление добавлено.`;
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

var parent = document.getElementById("appointmentForm");
parent.insertAdjacentHTML("beforeend", `
    <input type="hidden" id="user_id" value=${user_id}>
    <input type="hidden" id="group_id" value=${group_id}>
`);

function openForm() {
   console.log("asdasdsad")
  document.getElementById("loginPopup").style.display = "block";
}
function closeForm() {
  document.getElementById("loginPopup").style.display = "none";
}

===
Конец файла ===