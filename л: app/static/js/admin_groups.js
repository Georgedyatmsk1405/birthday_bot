```
// ... предыдущий код ...

function watchgroup(url) {
    console.log(url)
    window.location.href = url
}

function showCustomNotifications(group_id) {
    window.location.href = `custom_notifications?group_id=${group_id}&user_id=${user_id}`;
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
       text = '<table><tr><td>'+ val.name +'</td>' + 
              '<td><button onclick="funcctionName(\''+val.url+'\')" class="'+val.url+'">удалить группу</button></td>' +
              '<td><button onclick="watchgroup(\''+val.get_url+'\')" class="'+val.get_url+'">Посмотреть группу</button></td>' +
              '<td><button onclick="showCustomNotifications(\''+val.group_id+'\')" class="notif-btn-'+val.group_id+'">Уведомления</button></td></tr></table>'
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

```
