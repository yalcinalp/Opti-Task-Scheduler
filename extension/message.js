function getMessage() {
    var user = 'me';
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    var i = urlParams.get('message_no');
    fetch("http://127.0.0.1:5000/gmail/get_mail_no?user="+user+"&i="+i, {}).then(response => response.json()).then(data => { 
        document.getElementById("snippet").innerText=data["msg"];
    }
    ).catch(error => console.log(error));
}
getMessage();   