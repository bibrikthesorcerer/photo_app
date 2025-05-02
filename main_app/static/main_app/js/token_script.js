var csrf_token = document.currentScript.getAttribute('csrf_token')

var button_array = document.getElementsByClassName('token-btn');
button_array = [...button_array];

button_array.forEach(elem => {
    elem.addEventListener('click', function(event){
        generateToken(elem)
    }
    );
});

// function formatDate(date) {
//     const year = date.getFullYear();
//     const month = String(date.getMonth() + 1).padStart(2, '0');
//     const day = String(date.getDate()).padStart(2, '0');
//     const hours = String(date.getHours()).padStart(2, '0');
//     const minutes = String(date.getMinutes()).padStart(2, '0');
//     const seconds = String(date.getSeconds()).padStart(2, '0');
    
//     return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
// }

function generateToken(elem){
    $.ajax({
            url:'/generate_token/',
            type:'POST',
            data:{
                'csrfmiddlewaretoken': csrf_token,
            },
            success: function(response){
                console.log('SERVER RESPONDED:', response);
                const tokenDisplay = $("#userAPIToken");
                const tokenDate = $("#userAPITokenDate");
                date = new Date(response['created'])
                $(tokenDate).html(date);
                $(tokenDisplay).html(response['token']);
                $(".token-btn").html('Reissue API Token');
            },
            error: function(xhr){
                console.error('ERROR. SERVER RESPONDED:', JSON.parse(xhr.responseText).error);
            }
        });
}
