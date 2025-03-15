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
    switch (data.type){
        case ('notification'): 
            toast = $(createNotificationHTML(data.message, data.timestamp))
            $(toast).appendTo('#notificationContainer')
            $(toast).toast('show')
            break;
        case ('notify_like'):
            toast = $(createNotificationHTML(data.message, data.timestamp))
            $(toast).appendTo('#notificationContainer')
            $(toast).toast('show')
            // if user is currently viewing posts update likes count
            postsList = $('#postsList').get(0)
            if (postsList != undefined){
                post = $(postsList).find(`#${data.photo_id}`)
                like_btn = $(post).find(`.like-button`)
                $(like_btn).html(`${data.likes_count} ❤`);
                break;
            }
            // if user is viewing this photo on view_photo
            postContainer = $('#postContainer').get(0)
            if (postContainer != undefined){
                like_btn = $(postContainer).find('#likesCount')
                $(like_btn).html(`${data.likes_count} ❤`);
                break;
            }
            break;
        case ('notify_comment'):
            toast = $(createNotificationHTML(data.message, data.timestamp))
            $(toast).appendTo('#notificationContainer')
            $(toast).toast('show')
            // if user is currently viewing posts update comm count
            postsList = $('#postsList').get(0)
            if (postsList != undefined){
                post = $(postsList).find(`#${data.photo_id}`)
                comm_btn = $(post).find(`.comment-button`)
                $(comm_btn).html(`${data.comments_count} 🗨️`);
                break;
            }
            // if user is viewing this photo on view_photo
            postContainer = $('#postContainer').get(0)
            if (postContainer != undefined){
                comm_btn = $(postContainer).find('#commentsCount')
                $(comm_btn).html(`${data.comments_count} 🗨️`);
                break;
            }
            break;
        default:
            break;
    }
} 
