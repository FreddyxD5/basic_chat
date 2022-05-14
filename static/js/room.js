console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsersSelector.appendChild(newOption);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

onlineUsersSelector.onchange = function(){
    chatMessageInput.value = "/pm "+onlineUsersSelector.value +" ";
    onlineUsersSelector.value = null
    chatMessageInput.focus()
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    // TODO: forward the message to the WebSocket

    chatSocket.send(JSON.stringify({
        "message":chatMessageInput.value,
    }));
    chatMessageInput.value = "";
};


let chatSocket =null;

function connect(){
    chatSocket = new WebSocket("ws://"+window.location.host+"/ws/chatapp/"+roomName+'/')
    console.log(chatSocket)
    chatSocket.onopen = function(e){
        console.log("Se ha conectado correctamente")
             
    }

    chatSocket.onclose = function(e){
        console.log("WebSocket conexion cerrada inesperadamente. Tratando de reconectar...")
        setTimeout(function(){
            console.log('Reconectando...');
            connect();
        },2000);
    };

    chatSocket.onmessage = function (e){
        const data = JSON.parse(e.data)
        console.log(data)

        switch(data.type){
            case "chat_message":
                chatLog.value += data.user+":"+data.message + "\n"
                break;
            case "user_list":
                console.log("ther's always an undefined type?")
                for (let i=0;i<data.users.length;i++){                    
                    onlineUsersSelectorAdd(data.users[i]);
                }
            case "user_join":
                chatLog.value += data.user+" joined the room. \n"
                onlineUsersSelectorAdd(data.user)
                break;
            case "user_leave":
                chatLog.value += data.user +" left the room. \n"
                onlineUsersSelectorRemove(data.user);
                break;
            case "private_message":
                chatLog.value += "PM from"+data.user+" : "+data.message+"\n";
                break;
            case "private_message_delivered":
                chatLog.value += "PM to "+data.target+" : "+data.message+"\n";
                break;
            default:
                console.log("Tipo de mensaje desconocido what?")
                break;
            
        }   

        chatLog.scrollTo = chatLog.scrollHeight;
    }

    chatSocket.onerror = function(err){
        console.log("Websocket encountered an error"+ err.message);
        console.log("Cerrando socket")
        chatSocket.close();
    }

}


connect();