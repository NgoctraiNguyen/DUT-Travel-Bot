$(document).ready(function () {
    $('#post-form').submit(function (event) {
        const bodychat = document.getElementById('body-chat');
        event.preventDefault(); 


        const suggest_question_div_lasts = $('.suggest_questions');
        
        if (suggest_question_div_lasts.length > 0) {
            suggest_question_div_lasts.each(function () {
            $(this).remove();
            });
        }

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
            <div class="msg_suggest"> 
                <div> </div>
            </div>
            <div
        `;

        chatdiv1.innerHTML= chatconten1;
        bodychat.appendChild(chatdiv1);
        var inputchat=document.querySelector("#question");
        inputchat.value="";
        $('#body-chat').scrollTop($('#body-chat')[0].scrollHeight);

        var loadingText = ". . . . . . . .";
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
                
                div_message.innerHTML = "";
                var link_img_list = response.link_img;
                
                var tmp = "";

                if (link_img_list != "" && link_img_list != "None" && link_img_list != "['']") {
                        tmp += '<img src="' + link_img_list + '" alt="Image" width="50%" style="margin-right: 20px;">';
                }else {
                    tmp = ""
                }
                
                const words = response.answer.split(' ');

                const suggest_div = document.createElement('div');
                let suggest_question_item=`
                <div class="suggest_questions"></div>` 
                suggest_div.innerHTML=suggest_question_item;
                bodychat.appendChild(suggest_div);

                var suggest_question_div=document.querySelector(".suggest_questions");
                console.log(suggest_question_div)
                var suggest=response.suggest_text;
                var tmp_suggest="";
                suggest = suggest.slice(1, -1);

                // Chia chuỗi thành mảng dựa trên dấu ','
                var suggest_question = suggest.split(", ");
                console.log( typeof  suggest_question)
                console.log(   suggest_question)
                if (Array.isArray(suggest_question) && suggest_question.length > 0) {
                    for (var i = 0; i < suggest_question.length; i++) {
                        tmp_suggest += '<button class="suggest_questions_item" value="' + suggest_question[i] + '">' + suggest_question[i] + '</button>';
                    }
                } else {
                    tmp_suggest = "s";
                }
                
                clearInterval(interval);
                function displayWordsSequentially(index) {
                    if (index < words.length) {
                        div_message.innerHTML += words[index] + ' '; // Thêm từ vào div_message
                        index++; // Tăng chỉ số để hiển thị từ tiếp theo trong mảng
                
                        setTimeout(() => {
                            displayWordsSequentially(index); // Gọi lại hàm với từ tiếp theo sau một khoảng thời gian
                        }, 100); // Thời gian delay giữa các từ (ở đây là 1 giây)
                    }else{
                        if (tmp != "['']") {
                            div_message.innerHTML += " <br> " + tmp; 
                        }
                        if(tmp_suggest!=""){
                            suggest_question_div.innerHTML+="<br>"+tmp_suggest;

                        }
                    }
                }
                displayWordsSequentially(0)

                $('#body-chat').scrollTop($('#body-chat')[0].scrollHeight);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    });
});

$(document).ready(function () {
    // Xử lý sự kiện click trên các button suggest_questions_item

    $(document).on("click", ".suggest_questions_item", function (event) {
      event.preventDefault();
      
      // Lấy giá trị của button được nhấn
      var selectedValue = $(this).val();

      const suggest_question_div_last = $('.suggest_questions');
      console.log(suggest_question_div_last);
      if (suggest_question_div_last.length > 0) {
        suggest_question_div_last.each(function () {
          $(this).remove();
        });
      }
  
      // Gán giá trị vào trường input #question
      $('#question').val(selectedValue);
  
      // Submit form #post-form
      $('#post-form').submit();
    });
  
    // ...
  });