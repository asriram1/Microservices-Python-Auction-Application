// A user entered the username and what to join the chat room
username = "";
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


function  join_chat_success() {
    window.localStorage.setItem(window.chat_id + " session_token",this.responseText) ;
    window.localStorage.setItem(window.chat_id + " username",window.username) ;
    location.replace("chat/" + window.chat_id);

}