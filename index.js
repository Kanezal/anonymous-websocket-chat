var clientID = Date.now();
var ws = new WebSocket(`ws://localhost:8000/ws/${clientID}`);
const messagesScrollHeight = document.getElementById('messages').scrollHeight
const messageArea = document.getElementById("messageArea")

function processMessage(event) {
    var messages = document.getElementById('messages')
    var message = document.createElement('li')
    let data = JSON.parse(event.data).data

    message.classList += "list-group-item"
    message.innerHTML = `
    <div class="card ${data.client.id == clientID ? "text-white bg-success" : ""}" style="">
        <div class="card-header">${data.client.id}</div>
        <div class="card-body">
            <p class="card-text">${data.message.text}</p>
        </div>
    </div>
    `

    messages.appendChild(message);
    if (messages.scrollHeight > messagesScrollHeight && 
            messages.scrollTop + 60 + 300 > messages.scrollHeight - messagesScrollHeight) {
                messages.scrollTop = messages.scrollHeight;
    }
}

ws.onmessage = processMessage;

function sendMessage(event) {
    if (messageArea.innerHTML != "") {
        ws.send(messageArea.innerHTML);
    }

    messageArea.innerHTML = ''

    if (event) {
        event.preventDefault()
    }
}

function showForm(event) {
    var button = document.getElementById("connect");
    var form = document.getElementById("form");

    button.remove()
    form.style.display = "block";
}

messageArea.addEventListener("keydown", keyProcess)

function keyProcess(event) {
    if (event.code === "Enter" && !event.shiftKey) {
        event.preventDefault()
        sendMessage()
    }
}