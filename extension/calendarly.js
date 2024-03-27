var header = new Headers();
header.append("Content-Type", "application/json");

function getEvent() {
    fetch("http://127.0.0.1:5000/api/get_current", {}).then(response => response.json()).then(data => { 
        document.getElementById("EventName").innerText = data.event_name;
        document.getElementById("EventTime").innerText = data.event_time;
        document.getElementById("EventDescription").innerText = data.event_description;
    }
    ).catch(error => console.log(error));
}


function schedule() {
    fetch("http://127.0.0.1:5000/api/schedule", {}).
        then(response => response.json()).
        then(data => document.getElementById("status_bar").innerText = "Scheduled succesfully").
        catch(error => console.log(error));
}
function openTab() {
    window.open("https://calendar.google.com/calendar/u/0/r");
}

function deleteCalendar() {
    fetch("http://127.0.0.1:5000/api/delete_calendar", {}).
    then(response => response.json()).
    then(data => document.getElementById("status_bar").innerText = "Calendar deleted succesfully").
    catch(error => console.log(error));
}
document.getElementById("btn1").onclick = schedule;
document.getElementById("btn7").onclick = deleteCalendar;
document.getElementById("btn2").onclick = openTab;
getEvent();


