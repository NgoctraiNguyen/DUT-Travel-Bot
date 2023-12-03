const sentchatbtn = document.getElementById('submit');
const chatinput = document.getElementById('question');
const bodychat = document.getElementById('body-chat');


const createchatdiv = (message, classname) => {
    const chatdiv = document.createElement('div');

    if (classname === 'user-chat'){
        chatdiv.classList.add('d-flex', 'justify-content-end', 'chat-block', 'user-chat');
        let chatcontent = `<div class="user-msg"> ${message}</div>'`;
        chatdiv.innerHTML= chatcontent;
    }
    else{
        chatdiv.classList.add('d-flex', 'justify-content-start', '');
        let chatcontent = `
            <div class="bot-msg">
                . . .
            </div>
        `;
        chatdiv.innerHTML= chatcontent;
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