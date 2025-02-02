// static/js/session.js

const sessionID = "{{ session_id }}";  // Set dynamically from template
const socket = new WebSocket(`ws://${window.location.host}/ws/session/${sessionID}/`);

socket.onmessage = function (event) {
    const data = event.data;
    console.log("Received data:", data);
    const outputElement = document.getElementById("output");
    outputElement.innerHTML += `<p>${data}</p>`;
};

socket.onclose = function () {
    console.log("WebSocket connection closed.");
};