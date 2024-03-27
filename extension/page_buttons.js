document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('button1').addEventListener('click', function() {
        // document.getElementById('content').innerHTML = '<iframe src="calendarly.html" id="idIframe" width="100%" ></iframe>';
        window.location.assign("calendarly.html");
    });

    document.getElementById('button2').addEventListener('click', function() {
        // document.getElementById('content').innerHTML = '<iframe src="mailly.html" id="idIframe" width="100%" ></iframe>';
        window.location.assign("mailly.html");
    });
    
    document.getElementById('button3').addEventListener('click', function() {
        // document.getElementById('content').innerHTML = '<iframe src="mailly.html" id="idIframe" width="100%" ></iframe>';
        window.location.assign("form.html");
    });
    // Add more event listeners for additional buttons
});



