window.addEventListener("load", function () {
   document.getElementById("minhaDiv").classList.add("show");
   var elements = document.getElementsByClassName("fade-in-modo-edicao");
   if (elements.length > 0) {
      elements[0].classList.add("show");
   }
   document.getElementById("sair").classList.add("show_sair");
});
