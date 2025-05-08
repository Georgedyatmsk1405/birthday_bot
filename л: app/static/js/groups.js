```
// ... предыдущий код ...

fetch(`/api/groups?user_id=${user_id}`, {
    method: 'get',
    headers:{"Authorization": window.Telegram.WebApp.initData},
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
  div.innerHTML = "<strong>У вас нет групп </strong>";
  document.body.append(div);
  }
  if ("applications" in data){
  innerHTML = '<div class="child y proximity-scroll-snapping" dir="rtl">'
  for (val of data.applications) {
       text = '<table><tr><td>'+ val.name +'</td>' + 
              ' <td><button onclick="funcctionName(\''+val.url+'\')" class="'+val.url+'">покинуть группу</button></td>' +
              ' <td><button onclick="showCustomNotifications(\''+val.group_id+'\')" class="notif-btn-'+val.group_id+'">Уведомления</button></td></tr></table>'
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

function showCustomNotifications(group_id) {
    fetch(`/api/custom_notifications/${group_id}`, {
        method: 'get',
        headers: {"Authorization": window.Telegram.WebApp.initData},
    })
    .then(response => response.json())
    .then(notifications => {
        if (notifications.length > 0) {
            let notifHtml = '<div class="notifications-container">';
            notifications.forEach(notif => {
                notifHtml += `<div class="notification-item">
                    <p>${notif.message}</p>
                    <small>${new Date(notif.created_at).toLocaleString()}</small>
                </div>`;
            });
            notifHtml += '</div>';
            
            const popup = document.createElement('div');
            popup.className = 'notification-popup';
            popup.innerHTML = `
                <div class="popup-content">
                    <h3>Уведомления группы</h3>
                    ${notifHtml}
                    <button onclick="this.parentElement.parentElement.remove()">Закрыть</button>
                </div>
            `;
            document.body.appendChild(popup);
        } else {
            alert('В этой группе нет уведомлений');
        }
    })
    .catch(error => {
        console.error('Ошибка получения уведомлений:', error);
        alert('Не удалось загрузить уведомления');
    });
}

// Добавляем стили для уведомлений
const style = document.createElement('style');
style.textContent = `
.notification-popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}
.notification-popup .popup-content {
    background: white;
    padding: 20px;
    border-radius: 10px;
    max-width: 80%;
    max-height: 80%;
    overflow-y: auto;
}
.notifications-container {
    margin: 10px 0;
}
.notification-item {
    padding: 10px;
    border-bottom: 1px solid #eee;
}
.notification-item p {
    margin: 0 0 5px 0;
}
.notification-item small {
    color: #666;
}
`;
document.head.appendChild(style);

```
