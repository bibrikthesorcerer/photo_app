url = `ws://${window.location.host}/notify/`
notifySocket = new WebSocket(url)

function createNotificationHTML(message, timestamp){
    html_str = `<div class="toast text-bg-primary" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="false">
            <div class="toast-header">
                <strong class="me-auto">Notification (${timestamp})</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body fs-5">
                ${message}
            </div>
        </div>`
    return html_str
}

notifySocket.onmessage = function(e){
    data = JSON.parse(e.data)
    if (data.type === 'notification'){
        toast = $(createNotificationHTML(data.message, data.timestamp))
        $(toast).appendTo('#notificationContainer')
        $(toast).toast('show')
    }
} 
