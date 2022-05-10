const roomName = JSON.parse(document.getElementById('room-name').textContent);
const chatSocket = new WebSocket('ws://'+window.location.host+'/ws/chat/'+roomName+'/');
const userName = 'User-'+Math.floor(Math.random()*10000)
document.querySelector('#user-tag').textContent = '@'+userName
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);    
    document.querySelector('#chat-log').value += (userName+':   '+
    data.message+'\n')
};



document.querySelector('#chat-message-input').focus()
document.querySelector('#chat-message-input').onkeyup = function(e){            
    if (e.keyCode === 13){                console.log('Enter Press');
        document.querySelector('#chat-message-submit').click();
    }
}

document.querySelector('#chat-message-submit').onclick = function(e){            
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
            'message':message
    }));

    messageInputDom.value = '';
}

document.querySelector('#chat-disconnect').onclick = function(e){
    console.log('This is working?')
    chatSocket.close()
}
