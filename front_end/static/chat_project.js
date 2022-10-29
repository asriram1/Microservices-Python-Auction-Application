var ele1 = document.getElementById("create_chat_display");
var ele2 = document.getElementById("chat_room_display");
var ele3 = document.getElementById("join_chat_display");

var username = "";
var chat_id = "";

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
    window.chat_id = chat_id;
    document.getElementById("chat_room_display_chat_id").innerText = chat_id;
    /*var url = "/chat/"+chat_id;
    location.replace(url);*/
    chat_room_display();
}

function send_message() {
    console.log(window.chat_id);
    var getReq = new XMLHttpRequest();
    getReq.open("POST", "/api/messages");
    getReq.addEventListener("load", get_message);
    // oReq.setRequestHeader("Ocp-Apim-Subscription-Key","a5d9d1bfbba4442d98e393b08e2e9c2f");
    var message = document.getElementById("fname").value;

    var chat_id = window.chat_id;

    var username = localStorage.getItem(chat_id+" username");
    var session_token = localStorage.getItem(chat_id+" session_token");
    var dic = {
        "message": message
    };

    getReq.setRequestHeader("username",username);
    getReq.setRequestHeader("chat_id",chat_id);
    getReq.setRequestHeader("session_token",session_token);
    console.log("send" + JSON.stringify(dic));
    getReq.send(JSON.stringify(dic));
    request_message();
}

function request_message() {
    var oReq = new XMLHttpRequest();
    oReq.open("GET", "/api/messages");
    oReq.addEventListener("load", get_message);
    var message = document.getElementById("fname").value;

    var chat_id = window.chat_id;

    var username = localStorage.getItem(chat_id + " username");
    var session_token = localStorage.getItem(chat_id + " session_token");

    console.log(chat_id + " " + username + " " + session_token);
    oReq.setRequestHeader("username", username);
    oReq.setRequestHeader("chat_id", chat_id);
    oReq.setRequestHeader("session_token", session_token);
    oReq.send();
}

function get_message() {
    var text =  this.responseText;
    var obj = JSON.parse(text);
    console.log("get"+text);
    var messages = document.getElementById("messages");

    console.log(this.responseText);
    while(messages.firstChild){
        messages.removeChild(messages.firstChild);
    }

    for(var i in obj["messages"]) {
        var one_row = obj["messages"][i];
        console.log(one_row)
        var wrapper = document.createElement('div');

        if(one_row["username"] === username)
            wrapper.setAttribute('class','container darker');
        else
            wrapper.setAttribute('class','container');
        var p = document.createElement('p');
        p.innerHTML = one_row["body"] + " by " + one_row["username"];
        wrapper.appendChild(p);
        messages.appendChild(wrapper);
    }
}

function handle_creator_invite() {
    console.log(window.chat_id);
    var oReq = new XMLHttpRequest();

    var chat_id = window.chat_id;
    var session_token = localStorage.getItem(chat_id+" session_token");

    console.log(session_token);
    oReq.open("POST", "/api/"+chat_id+"/invite");
    oReq.setRequestHeader("session_token",session_token);
    oReq.addEventListener("load", creator_invite);
    oReq.send();
}

function creator_invite() {
    if(this.responseText==="")
        return;
    var invite = document.getElementById("invite");
    invite.innerHTML = "invite link: " + this.responseText;
}

// A user entered the username and what to join the chat room
function join_chat() {
    var chat_id = window.chat_id;
    // Authenticates the user by giving them a session token
    window.username = document.getElementById("name").value;
    var oReq = new XMLHttpRequest();
    oReq.open("POST", "/api/authenticate");
    oReq.addEventListener("load", join_chat_success);

    var magic_key = window.magic_key; //"some_magic_key";

    console.log(JSON.stringify({
                "username": username,
                "chat_id": chat_id,
                "magic_key": magic_key}));

    oReq.send(JSON.stringify({
                "username": username,
                "chat_id": chat_id,
                "magic_key": magic_key}));
}

function join_chat_success() {
    window.localStorage.setItem(window.chat_id + " session_token",this.responseText) ;
    window.localStorage.setItem(window.chat_id + " username",window.username) ;
    document.getElementById("chat_room_display_chat_id").innerText = window.chat_id;

    chat_room_display();
    // location.replace("chat/" + window.chat_id);
}

function create_chat_display() {
    ele1.style.display = 'block';
    ele2.style.display = 'none';
    ele3.style.display = 'none';
}

function chat_room_display() {
    ele1.style.display = 'none';
    ele2.style.display = 'block';
    ele3.style.display = 'none';
    setInterval(request_message, 500);
    handle_creator_invite();
    history.pushState({},"","/chat/"+chat_id);
}

function join_chat_display() {
    ele1.style.display = 'none';
    ele2.style.display = 'none';
    ele3.style.display = 'block';

}