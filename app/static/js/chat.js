const sentchatbtn = document.getElementById('submit');
const chatinput = document.getElementById('question');
const bodychat = document.getElementById('body-chat');


const createchatdiv = (message, classname) => {
    const chatdiv = document.createElement('div');

    if (classname === 'user-chat'){
        const url_user_image = document.getElementById('user-image').src;
        chatdiv.classList.add('d-flex', 'justify-content-end', 'mb-4', 'user-chat');
        let chatconten = `<div class="msg_cotainer_send"> ${message}</div><div class="img_cont_msg"><img src="${url_user_image}" class="rounded-circle user_img_msg"></div>'`;
        chatdiv.innerHTML= chatconten;
    }
    else{
        const url_bot_image = document.getElementById('bot-image').src;
        chatdiv.classList.add('d-flex', 'justify-content-start', 'mb-4');
        let chatconten = `
            <div class="img_cont_msg">
                <img id="bot-image" src="${url_bot_image}" class="rounded-circle user_img_msg">
            </div>
            <div class="msg_cotainer">
                . . .
            </div>
        `;
        chatdiv.innerHTML= chatconten;
    }
    return chatdiv;
}

const handleChat = () =>{
    const question = chatinput.value.trim();
    if(!question) return;

    bodychat.appendChild(createchatdiv(question, 'user-chat'));
    bodychat.appendChild(createchatdiv(question, 'bot-chat'));
    $('#body-chat').scrollTop($('#body-chat')[0].scrollHeight);
}

sentchatbtn.addEventListener('click', handleChat);