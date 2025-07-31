var csrf_token = document.currentScript.getAttribute('csrf_token')
likeButtons = document.getElementsByClassName('like-button');
likeButtonsArray = [...likeButtons];

likeButtonsArray.forEach((elem) => {
    elem.addEventListener('click', function(event){
        likeAJAX(elem)
    }
    );
})

function likeAJAX(elem){
    elem.disabled = true
    photo_id = elem.getAttribute('data-photo-id')
    if (elem.classList.contains('text-bg-primary')){
        createLikeAJAX(elem, photo_id);
    }
    else if(elem.classList.contains('text-bg-danger')){
        removeLikeAJAX(elem, photo_id);
    }
}

function createLikeAJAX(elem, photo_id){
    $.ajax({
            url:'/create_like/',
            type:'POST',
            data:{
                'csrfmiddlewaretoken': csrf_token,
                'photo_id':photo_id
            },
            success: function(response){
                console.log('SERVER RESPONDED:', response);
                elem.classList.remove('text-bg-primary');
                elem.classList.add('text-bg-danger');
                numOfLikes = parseInt(elem.innerHTML.match(/(\d+)/)[0]);
                numOfLikes++;
                elem.innerHTML = '' + numOfLikes + ' ❤';
                elem.disabled = false;
            },
            error: function(xhr){
                console.error('ERROR. SERVER RESPONDED:', JSON.parse(xhr.responseText).error);
                if (xhr.status === 403){
                    toast = $('#permissionDenied')
                    $(toast).find(".toast-body:first").html(xhr.responseJSON.message)
                    $(toast).toast('show');
                }
                elem.disabled = false;
            }
        });
}

function removeLikeAJAX(elem, photo_id){
    $.ajax({
            url:'/remove_like/',
            type:'POST',
            data:{
                'csrfmiddlewaretoken': csrf_token,
                'photo_id':photo_id
            },
            success: function(response){
                console.log('SERVER RESPONDED:', response);
                elem.classList.remove('text-bg-danger');
                elem.classList.add('text-bg-primary');
                numOfLikes = parseInt(elem.innerHTML.match(/(\d+)/)[0]);
                numOfLikes--;
                elem.innerHTML = '' + numOfLikes + ' ❤';
                elem.disabled = false;
            },
            error: function(xhr){
                console.error('ERROR. SERVER RESPONDED:', JSON.parse(xhr.responseText).error);
                if (xhr.status === 403){
                    toast = $('#permissionDenied')
                    $(toast).find(".toast-body:first").html(xhr.responseJSON.message)
                    $(toast).toast('show');
                }
                elem.disabled = false;
            }
        });
}

