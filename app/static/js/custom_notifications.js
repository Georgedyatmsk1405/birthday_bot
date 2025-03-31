javascript
document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/custom_notifications/')
        .then(response => response.json())
        .then(notifications => {
            const container = document.getElementById('notifications');
            notifications.forEach(notification => {
                const item = document.createElement('div');
                item.textContent = notification.content;
                container.appendChild(item);
            });
        });
});
