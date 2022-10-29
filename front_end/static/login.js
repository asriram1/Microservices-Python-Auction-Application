function login() {
    var getReq = new XMLHttpRequest();
    getReq.open("POST", "/api/login");
    getReq.addEventListener("load", login_message);
    var email = document.getElementById("login_email").value;
    var password = document.getElementById("login_password").value;
    localStorage.setItem("user_email", email);
    console.log("login: ");
    console.log(email);
    console.log(password);
    getReq.send(JSON.stringify({
        "email": email,
        "password": password}));
}

function login_message() {
    var text = JSON.parse(this.responseText);
    console.log(text);

    // window.localStorage.setItem(window.chat_id + " session_token",this.responseText) ;
    // window.localStorage.setItem(window.chat_id + " username",window.username) ;
    if(text["success"] == true) {
        location.replace("main_page");
        localStorage.setItem("user_key",text["user_key"]);
    } else {
        document.getElementById("login_error").innerText = "Login failed, please check your email and password!";
    }
    
    // if(text["login_code"] == "true") {
    //     console.log("login success");
    //     window.session_token = text["session_token"];
    //     window.username = text["username"];
    //     belay_display();
    // }
    // else {
    //     document.getElementById("login_error").innerText = "email or password not correct, please try again";
    // }

}

function register() {
     var getReq = new XMLHttpRequest();
     getReq.open("PUT", "/api/register");
     getReq.addEventListener("load", register_message);
     // oReq.setRequestHeader("Ocp-Apim-Subscription-Key","a5d9d1bfbba4442d98e393b08e2e9c2f");
 
     var email = document.getElementById("login_email").value;
     var password = document.getElementById("login_password").value;
    
     console.log("register: ");
     console.log(email);
     console.log(password);

     getReq.send(JSON.stringify({
        "email": email,
        "password": password}));
 }
 
 
 
 function register_message() {
    var text = JSON.parse(this.responseText);
    console.log(text);
    if(text["success"] == true) {
        document.getElementById("login_error").innerText = "Register succeed!";
    } else {
        document.getElementById("login_error").innerText = "Register failed!";
    }
    //  if(text["register_code"] == "true") {
    //      console.log("register success");
    //      login_display();
    //  }
    //  else {
    //      document.getElementById("register_error").innerText = "This email has been registered, please use another email or login";
    //  }
}