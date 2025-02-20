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


function funcctionName (url) {
	const paragraph = document.getElementsByClassName(url);
	console.log(paragraph)

	var isAdmin = confirm("Вы уверены что хотите удалить группу?");

    console.log(isAdmin)

    if (isAdmin===true) {
          console.log(":asdasdasdasd")
          fetch(url, {
            method: 'delete',
            headers:{"Authorization": window.Telegram.WebApp.initData}
        }).then(response => {
    if (!response.ok) {
      console.log(response.status)
      console.log(response.status)
      throw new Error(`Ошибка сети: ${response.status}`);
    }
    window.location.href = `admin_groups?&user_id=${user_id}`
  })
  .then(data => console.log(data))
  .catch(error => {
    console.error('Произошла ошибка:', error);
    alert('Не удалось загрузить данные. Пожалуйста, попробуйте позже.');
  });
    } else {
       console.log("esesesazzzzzzzzz");
    }


}
function watchgroup (url) {
    console.log(url)
    window.location.href = url

}
fetch(`/api/admin_groups?user_id=${user_id}`, {
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
  div.innerHTML = "<strong>У вас нет администрируемых групп </strong>";
  document.body.append(div);
  }
  if ("applications" in data){
  innerHTML = '<div class="child y proximity-scroll-snapping" dir="rtl">'
  for (val of data.applications) {
       text = '<table><tr><td>'+ val.name +'</td>' + '<td><button onclick="funcctionName(\''+val.url+'\')" class="'+val.url+'">удалить группу</button></td>'+ '<td><button onclick="watchgroup(\''+val.get_url+'\')" class="'+val.get_url+'">Посмотреть группу</button></td></tr></table>'
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
