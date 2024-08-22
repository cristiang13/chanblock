// // websocket-handler.js
// // Establece la conexión WebSocket con el servidor Django 
// console.log('Script cargado');
// const webSocket = new WebSocket('ws://127.0.0.1:8000/ws/vara/');

// console.log('Conectando...');
// webSocket.onopen = function(event) {
//     console.log('*****Conexión WebSocket establecida.');
// };

// webSocket.onerror = function(event) {
//     console.error('Error en la conexión WebSocket:', event);
// };

// webSocket.onclose = function(event) {
//     console.log('Conexión WebSocket cerrada:', event);
// };

// webSocket.onmessage = function(event) {
//     console.log("Mensaje recibido frontend:", event.data);
//     const blocks = JSON.parse(event.data);
//     // updateBlockDisplay(blocks);
// };

// websocket-handler.js

console.log('Script cargado');
let webSocket;
let reconnectInterval = 5000; // Tiempo en milisegundos para intentar reconectar

function connectWebSocket() {
    webSocket = new WebSocket('ws://127.0.0.1:8081/ws/vara/');
    // webSocket = new WebSocket('wss://chanblock.com/ws/vara/');

    webSocket.onopen = function(event) {
        console.log('*****Conexión WebSocket establecida.');
    };

    webSocket.onerror = function(event) {
        console.error('Error en la conexión WebSocket:', event);
    };

    webSocket.onclose = function(event) {
        console.log('Conexión WebSocket cerrada:', event);
        // Intentar reconectar
        setTimeout(connectWebSocket, reconnectInterval);
    };

    webSocket.onmessage = function(event) {
        console.log("Mensaje recibido frontend:", event.data);
        const blocks = JSON.parse(event.data);
        // updateBlockDisplay(blocks);
    };
}

// Conectar por primera vez
connectWebSocket();

// Función para verificar el estado del WebSocket
function checkWebSocketOpen() {
    if (webSocket.readyState === WebSocket.OPEN) {
        console.log("WebSocket está abierto.");
    } else {
        console.log("WebSocket no está abierto. Estado actual:", webSocket.readyState);
    }
}

// Verificar el estado del WebSocket cada 10 segundos
setInterval(checkWebSocketOpen, 10000);

