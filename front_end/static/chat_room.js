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

    console.log(JSON.stringify(dic));
    getReq.send(JSON.stringify(dic));

    request_message();
}

setInterval(request_message, 500);
handle_creator_invite();

function request_message() {
    var oReq = new XMLHttpRequest();
    oReq.open("GET", "/api/messages");
    oReq.addEventListener("load", get_message);
    var message = document.getElementById("fname").value;

    var chat_id = window.chat_id;

    var username = localStorage.getItem(chat_id+" username");
    var session_token = localStorage.getItem(chat_id+" session_token");

    console.log(chat_id+" "+username+" "+session_token);
    oReq.setRequestHeader("username",username);
    oReq.setRequestHeader("chat_id",chat_id);
    oReq.setRequestHeader("session_token",session_token);

    oReq.send();

}
// <script> window.chat_id ={{ chat_id}} </script>
function get_message() {
    var text =  this.responseText;
    var obj = JSON.parse(text);
    var messages = document.getElementById("messages");

    console.log(this.responseText);
    while(messages.firstChild){
        messages.removeChild(messages.firstChild);
    }

    for(var i in obj["messages"]) {
        var one_row = obj["messages"][i];
        console.log(one_row)
        var wrapper = document.createElement('div');

        wrapper.setAttribute('class','container darker');

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