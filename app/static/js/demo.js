

$(document).ready(function () {
    $('#post-form').submit(function (event) {
        const bodychat = document.getElementById('body-chat');
        event.preventDefault(); 

        if (question === "") return;

        const suggest_question_div_lasts = $('.suggest_questions');
        
        if (suggest_question_div_lasts.length > 0) {
            suggest_question_div_lasts.each(function () {
            $(this).remove();
            });
        }

        var question = $('#question').val();
        var tag = $('#tag').val();
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        
        const chatdiv = document.createElement('div');
        chatdiv.classList.add('d-flex', 'justify-content-end', 'chat-block', 'user-chat');
        let chatconten = `<div class="user-msg"> ${question}</div>`;
        chatdiv.innerHTML= chatconten;
        bodychat.appendChild(chatdiv);


        const chatdiv1 = document.createElement('div');
        chatdiv1.classList.add('d-flex', 'justify-content-start', 'chat-block');


        let chatconten1 = `
            <div class="bot-msg">
                <div class="loading"></div>
            </div>
            <div class="msg_suggest">
            </div>
        `;

        chatdiv1.innerHTML= chatconten1;
        bodychat.appendChild(chatdiv1);
        var inputchat=document.querySelector("#question");
        inputchat.value="";
        $('#body-chat').scrollTop($('#body-chat')[0].scrollHeight);

        var loadingText = ".  .  .  .  .  .  .  .";
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
                        tmp += '<br> <br> <img src="' + link_img_list + '" alt="Image" width="50%" style="margin-right: 20px;">';
                }else {
                    tmp = ""
                }
                
                const words = response.answer.split(' ');

                const suggest_div = document.createElement('div');
                // suggest_div.classList.add('msg_suggest')
                // bodychat.appendChild(suggest_div);
                let suggest_question_item=`
                <div class="suggest_questions"></div>` 
                suggest_div.innerHTML=suggest_question_item;
                bodychat.appendChild(suggest_div);

                var suggest_question_div=document.querySelector(".suggest_questions");
                var suggest=response.suggest_text;
                var tmp_suggest="";
                suggest = suggest.slice(1, -1);

                // Chia chuỗi thành mảng dựa trên dấu ','
                var suggest_question = suggest.split(", ");

                if (Array.isArray(suggest_question) && suggest_question.length > 0) {
                    // Xáo trộn thứ tự trong mảng
                    suggest_question.sort(() => Math.random() - 0.5);
                  
                    var tmp_suggest = '';
                    var numElements = suggest_question.length >= 3 ? 3 : suggest_question.length; // Số phần tử cần lấy (tối đa 3 hoặc độ dài của mảng)


                    for (var i = 0; i < numElements; i++) {
                        let question_temp = suggest_question[i];
                        tmp_suggest += `
                          <div class="suggest_questions d-flex justify-content-end chat-block">
                            <button class="suggest_questions_item" value="${question_temp.slice(1,-1)}">${question_temp.slice(1,-1)}</button>
                          </div>
                        `;
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
                            div_message.innerHTML += tmp; 
                        }
                        if(tmp_suggest!=""){
                            suggest_question_div.innerHTML+=tmp_suggest;

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