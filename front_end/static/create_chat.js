var username = "";

function create_chat() {
    var username = document.getElementById("create_chat").value;
    console.log(username);
    window.username = username;
    var oReq = new XMLHttpRequest();
    oReq.open("POST", "/api/create");
    oReq.addEventListener("load", create_chat_success);
    oReq.send(username);
}

function create_chat_success() {
    console.log(this.responseText);
    var create_success_board = document.getElementById("create_chat_success");
    var text = JSON.parse(this.responseText);
    create_success_board.innerText = "Create success, chat id is " +  text["chat_id"];
    create_success_board.innerText += " Magic link is: " +  text["magic_invite_link"];
    var chat_id = text["chat_id"];
    var session_token = text["session_token"];
    localStorage.setItem(chat_id+" session_token",session_token);
    localStorage.setItem(chat_id+" username",window.username);
    var url = "/chat/"+chat_id;
    location.replace(url);
}

