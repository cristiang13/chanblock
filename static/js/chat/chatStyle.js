var chatBox = document.querySelector('.chat-box');
var chatIcon = document.querySelector('.chat-icon');

chatIcon.addEventListener('click', function() {
  chatBox.classList.toggle('active');
  chatIcon.style.display = 'none'; // Ocultar el icono del chat
});

document.querySelector('.toggle-chat').addEventListener('click', function() {
  chatBox.classList.toggle('active');
  chatIcon.style.display = 'block'; // Mostrar el icono del chat
});