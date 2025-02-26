// Obtendo os elementos do DOM
let modal = document.getElementById("myModal");
let openModalBtn = document.getElementById("openModalBtn");
let closeModalBtn = document.getElementById("closeModalBtn");

// Abrir o modal quando o botão for clicado
openModalBtn.onclick = function() {
    modal.style.display = "block";
}

// Fechar o modal quando o botão (X) for clicado
closeModalBtn.onclick = function() {
    modal.style.display = "none";
}

// Fechar o modal se o usuário clicar fora do conteúdo do modal
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
