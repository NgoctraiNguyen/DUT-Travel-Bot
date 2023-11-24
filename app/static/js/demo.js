$(document).ready(function () {
    $('#post-form').submit(function (event) {
        const bodychat = document.getElementById('body-chat');
        event.preventDefault(); 

        var question = $('#question').val();
        var tag = $('#tag').val();
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        if (question === "") return;
        
        const chatdiv = document.createElement('div');
        const url_user_image = document.getElementById('user-image').src;
        chatdiv.classList.add('d-flex', 'justify-content-end', 'mb-4', 'user-chat');
        let chatconten = `<div class="msg_cotainer_send"> ${question}</div><div class="img_cont_msg"><img src="${url_user_image}" class="rounded-circle user_img_msg"></div>'`;
        chatdiv.innerHTML= chatconten;
        bodychat.appendChild(chatdiv);

        const chatdiv1 = document.createElement('div');
        const url_bot_image = document.getElementById('bot-image').src;
        chatdiv1.classList.add('d-flex', 'justify-content-start', 'mb-4');
        let chatconten1 = `
            <div class="img_cont_msg">
                <img id="bot-image" src="${url_bot_image}" class="rounded-circle user_img_msg">
            </div>
            <div class="msg_cotainer">
                <div class="loading"></div>
            </div>
            <div
        `;
        chatdiv1.innerHTML= chatconten1;
        bodychat.appendChild(chatdiv1);
        var inputchat=document.querySelector("#question");
        inputchat.value="";
        $('#body-chat').scrollTop($('#body-chat')[0].scrollHeight);

        const count = 0;

        var loadingText = ". . . .";
        var index = 0;
        var interval = setInterval(function() {
          $('.loading').last().text(loadingText.substring(0, index));
          index++;
          if (index > loadingText.length) {
              clearInterval(interval);
          }
        }, 300);

        $.ajax({
            type: 'POST',
            url: '/predict/', 
            data: {
                'question': question,
                'tag':tag,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function (response) {
                const div_messages = document.querySelectorAll('.loading');
                var div_message = div_messages[div_messages.length - 1];
                
                console.log(div_message)
                div_message.innerHTML = "";
                var link_img_list = response.link_img;
                var tmp = "";
                if (link_img_list != "") {
                        tmp += '<img src="' + link_img_list + '" alt="Image" width="50%" style="margin-right: 20px;">';
                }
                else{
                    tmp = ""
                }
                clearInterval(interval);
                div_message.innerHTML = response.answer +" <br> " + tmp;                   

                console.log(div_message)
                $('#body-chat').scrollTop($('#body-chat')[0].scrollHeight);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    });
});