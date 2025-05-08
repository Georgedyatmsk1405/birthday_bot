```javascript
const urlParams = new URLSearchParams(window.location.search);
const group_id = urlParams.get('group_id');
const user_id = urlParams.get('user_id');

document.addEventListener('DOMContentLoaded', () => {
    fetchNotifications();
    setupForm();
});

async function fetchNotifications() {
    try {
        const response = await fetch(`/api/custom-notifications/group/${group_id}`, {
            headers: {"Authorization": window.Telegram.WebApp.initData}
        });
        
        if (!response.ok) throw new Error('Failed to fetch notifications');
        
        const data = await response.json();
        renderNotifications(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load notifications');
    }
}

function renderNotifications(notifications) {
    const container = document.getElementById('notifications-container');
    container.innerHTML = '';
    
    if (!notifications || notifications.length === 0) {
        container.innerHTML = '<p>No notifications found</p>';
        return;
    }
    
    notifications.forEach(notification => {
        const card = document.createElement('div');
        card.className = 'notification-card';
        card.innerHTML = `
            <p>${notification.message}</p>
            <div class="notification-actions">
                <button onclick="editNotification(${notification.id})">Edit</button>
                <button onclick="deleteNotification(${notification.id})">Delete</button>
            </div>
        `;
        container.appendChild(card);
    });
}

function setupForm() {
    const form = document.getElementById('notification-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = document.getElementById('message').value.trim();
        if (!message) {
            alert('Message is required');
            return;
        }
        
        try {
            const response = await fetch('/api/custom-notifications', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": window.Telegram.WebApp.initData
                },
                body: JSON.stringify({
                    group_id: parseInt(group_id),
                    message: message
                })
            });
            
            if (!response.ok) throw new Error('Failed to create notification');
            
            document.getElementById('message').value = '';
            fetchNotifications();
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to create notification');
        }
    });
}

async function editNotification(id) {
    const newMessage = prompt('Enter new message:');
    if (!newMessage) return;
    
    try {
        const response = await fetch(`/api/custom-notifications/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": window.Telegram.WebApp.initData
            },
            body: JSON.stringify({
                message: newMessage
            })
        });
        
        if (!response.ok) throw new Error('Failed to update notification');
        
        fetchNotifications();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to update notification');
    }
}

async function deleteNotification(id) {
    if (!confirm('Are you sure you want to delete this notification?')) return;
    
    try {
        const response = await fetch(`/api/custom-notifications/${id}`, {
            method: 'DELETE',
            headers: {"Authorization": window.Telegram.WebApp.initData}
        });
        
        if (!response.ok) throw new Error('Failed to delete notification');
        
        fetchNotifications();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to delete notification');
    }
}
```
