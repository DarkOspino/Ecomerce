
document.getElementById("btn__registrarse").addEventListener("click" , register);
document.getElementById("btn__iniciar-sesion").addEventListener("click" , iniciarSesion);


window.addEventListener("rezisa", anchoPagina);
//declarando variavles

var contenedor_login_register = document.querySelector(".formulario__login-register");
var formulario_login =          document.querySelector(".formulario__login");
var formulario_register =       document.querySelector(".formulario__register");
var caja_trasera_login =        document.querySelector(".caja__trasera-login");
var caja_trasera_register =     document.querySelector(".caja__trasera-register");


function anchoPagina(){
    if(window.innerWidth > 850){
        caja_trasera_login.style.display = "block";
        caja_trasera_register.style.display = "block";

    }else{
        caja_trasera_register.style.display = "block";
        caja_trasera_register.style.opacity = "1";
        caja_trasera_login.style.display = "none";
        formulario_login.style.display = "block";
        formulario_register.style.display = "none";
        contenedor_login_register.style.left = "0px";
    }
}

anchoPagina();
function iniciarSesion(){

    if(window.innerWidth > 850){
        formulario_register.style.display ="none";
        formulario_register.style.left = "10px";
        formulario_login.style.display = "block";
        caja_trasera_register.style.opacity = "1";
        caja_trasera_login.style.opacity = "0";
    }else{
        formulario_register.style.display ="none";
        formulario_register.style.left = "0px";
        formulario_login.style.display = "block";
        caja_trasera_register.style.display = "block";
        caja_trasera_login.style.opacity = "none";
    }
    

    }
    
function register(){
    if(window.innerWidth > 850){
        formulario_register.style.display = "block";
        formulario_register.style.opacity = "1";
        formulario_register.style.left = "410px";
        formulario_login.style.display = "none";
        caja_trasera_register.style.opacity = "0";
        caja_trasera_login.style.opacity = "1";
    }else{
        formulario_register.style.display ="block";
        formulario_register.style.left = "0px";
        formulario_login.style.display = "none";
        caja_trasera_register.style.display = "none";
        caja_trasera_login.style.opacity = "block";
        caja_trasera_login.style.opacity = "1";
    }


}

var ProductImg = document.getElementById("ProductImg");
var SmallImg = document.getElementsByClassName("small-img");

SmallImg[0].onclick = function(){
    ProductImg.src = SmallImg[0].src;
}
SmallImg[1].onclick = function(){
    ProductImg.src = SmallImg[1].src;
}
SmallImg[2].onclick = function(){
    ProductImg.src = SmallImg[2].src;
}
SmallImg[3].onclick = function(){
    ProductImg.src = SmallImg[3].src;
}