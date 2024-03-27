function addEmail() {
    // Define the URL where the POST request will be sent
    const url = 'http://127.0.0.1:5000/gmail/add_user';

    // Create an object with the data you want to send
    const data = {
        user: 'me',
        email: document.getElementById("emailInput").value
    };

    // Use the fetch API to make the POST request
    fetch(url, {
        method: 'POST',     // Specify the method
        headers: {
            'Content-Type': 'application/json',  // Set the content type header
        },
        body: JSON.stringify(data)  // Convert the JavaScript object to a JSON string
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        console.log('Success:', data);  // Handle the success case
    })
    .catch((error) => {
        console.error('Error:', error);  // Handle errors
    });

}
var i = 0;
var len = 0;

function deleteAccount() {
    var user = 'me';
    const url = 'http://127.0.0.1:5000/gmail/get_accounts?user=' + user;
    fetch(url, {headers: {'Content-Type': 'application/json'}}).
        then(response => response.json()).then(response => {}).catch(error => console.log(error));
}


function getAccounts() {
    var user = 'me';
    const url = 'http://127.0.0.1:5000/gmail/get_accounts?user=' + user;fetch(url, {headers: {'Content-Type': 'application/json'}}).
    then(response => response.json()).
    then(response => {
        var accounts= response["accounts"];
        var obj = document.getElementById("emailList");
        if(obj !=null){
            document.getElementById("emailList").remove();
            var element = document.createElement("div"); 
            document.getElementById("inbox").innerHTML += "<div id='accountList'></div>";
            for(var i = 0; i < accounts.length; i++)
            {
                document.getElementById("accountList").innerHTML += "<p>"+accounts[i]+"</p>";
            }
        }  
    }).
    catch(error => console.log(error));
}



function button_setter() {prev_button = document.getElementById("btnprev");
next_button = document.getElementById("btnnext");
if(prev_button != null)
    prev_button.addEventListener("click", function() {
        if(i > 0)
        {i--;
        document.getElementById("emailList").innerHTML = "<iframe src='message.html?message_no=" + i + "'></iframe><p>"+(i+1)+"/"+len+"</p><button id='btnprev'> \< </button><button id='btnnext'> \></button>";}
        button_setter();
    });
if(next_button != null)
    next_button.addEventListener("click", function() {
        if(i < len -1 )    
        {i++;
        document.getElementById("emailList").innerHTML = "<iframe src='message.html?message_no=" + i + "'></iframe><p>"+(i+1)+"/"+len+"</p><button id='btnprev'> \< </button><button id='btnnext'> \></button>";}
        button_setter();        
    });}

function getEmails() {
    user= 'me';
    fetch("http://127.0.0.1:5000/gmail/get_mails?user=" + user, {headers: {'Content-Type': 'application/json'}}).
        then(response => response.json()).then(messages => {
                len = messages.length;
                if(len > 0){
                    document.getElementById("emailList").innerHTML = "<iframe src='message.html?message_no=" + i + "'></iframe><p>"+(i+1)+"/"+len+"</p><button id='btnprev'> \< </button><button id='btnnext'> \></button>";}

                }
    ).then( None => {
        if(document.getElementById("emailList") != null)
            button_setter();
        }
        ).catch(error => console.log(error));
}

function Refresh() {
    var obj = documents.getElementById("accountList");
    if(obj != null){
        while(obj.firstChild){
            obj.removeChild(obj.firstChild);
        }
        document.getElementById("accountList").remove();
        document.getElementById("inbox").innerHTML = "<h2>Inbox</h2><div id='emailList'>No emails yet.</div>";
    }
    getEmails();
}

document.getElementById("btn3").onclick = addEmail;
document.getElementById("btn4").onclick = Refresh;
document.getElementById("btn8").onclick = getAccounts;
document.getElementById("btn9").onclick = deleteAccount;
getEmails();
