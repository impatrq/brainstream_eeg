let logochange = document.getElementById("logochange");
window.addEventListener("scroll", function(){
    var header = document.querySelector("header");
    header.classList.toggle("sticky",window.scrollY > 0);
    if(50>window.scrollY > 0){
        logochange.src = "/static/img/logo-negro.png";
    }
    if(window.scrollY == 0){
        logochange.src = "/static/img/logo.png";
    }
})

