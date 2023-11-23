$(document).ready(function () {
    $('#post-form').submit(function (event) {
        
        const sentchatbtn = document.getElementById('submit');
        const chatinput = document.getElementById('question');
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
                <div id="loading"></div>
            </div>
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
          $('#loading').text(loadingText.substring(0, index));
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
                // Khi nhận được phản hồi từ máy chủ
                const div_message = document.getElementById('loading');
                const loadingDiv = document.createElement('div');
                loadingDiv.id = 'loading'+count;
                // div_message.innerHTML = response.result;
                loadingDiv.textContent = response.result;
                div_message.appendChild(loadingDiv);
                count+=1;
                $('#body-chat').scrollTop($('#body-chat')[0].scrollHeight);
                clearInterval(interval);
            },
            error: function (xhr, errmsg, err) {
                // Xử lý lỗi nếu có
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    });
});