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
const urlParams = new URLSearchParams(window.location.search);
const group_id = urlParams.get('group_id');
const user_id = urlParams.get('user_id');
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


function funccctionName (url) {
    console.log(url)
	const paragraph = document.getElementsByClassName(url);
	console.log(paragraph)

	var isAdmin = confirm("Вы уверены что хотите удалить пользователя?");
    console.log(isAdmin)
    if (isAdmin===true) {
          console.log(":asdasdasdasd")
          fetch(url, {
            method: 'delete',
        })
        window.location.href = `group_users?group_id=${group_id}&user_id=${user_id}`;
    } else {
       console.log("esesesazzzzzzzzz");

    }
    console.log("zlklllllllll")

}

fetch(`/api/group_users?user_id=${user_id}&group_id=${group_id}`, {
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
  div.innerHTML = "<strong>В этой группе нет пользователей </strong>";
  document.body.append(div);
  }
  if ("applications" in data){
  innerHTML = '<div class="child y proximity-scroll-snapping" dir="rtl">'
  for (val of data.applications) {
       text = '<table><tr><td>'+ val.name +'</td>'+'<td>'+ val.birth_date + '</td> <td><button onclick="funccctionName(\''+val.url+'\')" class="'+val.url+'">удалить пользователя</button></td></tr></table>'
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
function fetchinvite()  {
const urlParams = new URLSearchParams(window.location.search);
const myParam = urlParams.get('group_id');
console.log(myParam)

        fetch("api/group/invite/" + myParam, {
            method: 'post',
            headers:{"Authorization": window.Telegram.WebApp.initData}
        }).then(response => {
    if (!response.ok) {
      console.log(response.status)
      console.log(response.status)
      throw new Error(`Ошибка сети: ${response.status}`);
    }

    return response.json();
  })
  .then(data => {console.log(data)
  let input = document.createElement('input');
  input.value = data.token
  input.id="token"
  input.type="text"
  input.style="display: none"
  document.body.append(input);
    const popupMessage = `токен для группы -${data.token}`;
    document.getElementById('popupMessage').textContent = popupMessage;

    document.getElementById('popup').style.display = 'flex';})
  .catch(error => {
    console.error('Произошла ошибка:', error);
    alert('Не удалось загрузить данные. Пожалуйста, попробуйте позже.');
  });

    console.log("zlklllllllll")

}
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
        group_name: name,
        user_id: userId,
        group_id: group_id,
        notification_interval:notification_interval,
    };

    // Преобразуем объект в JSON строку
    const jsonData = JSON.stringify(appointmentData);
    fetch('/api/group', {
    method: 'put',
    headers:{"Authorization": window.Telegram.WebApp.initData},
    body: jsonData,
})
.then(response => {
    if (!response.ok) {
      console.log(response.status)
      console.log(response.status)
      throw new Error(`Ошибка сети: ${response.status}`);
    }
    window.location.href = `group_users?group_id=${group_id}&user_id=${user_id}`
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
function copyFunction() {
  var copyText = document.getElementById("token");
  copyText.select();
  copyText.setSelectionRange(0, 99999)
  document.execCommand("copy");
  alert("Токен скопирован: " + copyText.value);
}
function openForm() {
   console.log("asdasdsad")
  document.getElementById("loginPopup").style.display = "block";
}
function closeForm() {
  document.getElementById("loginPopup").style.display = "none";
}