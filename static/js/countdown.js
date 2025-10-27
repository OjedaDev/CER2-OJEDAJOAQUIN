
document.addEventListener("DOMContentLoaded", () => {


    const contenedores = document.querySelectorAll(".countdown-timer");


    if (contenedores.length === 0) return;


    const iniciarCountdown = (contenedor) => {
        

        const fechaEvento = new Date(contenedor.dataset.fecha).getTime();

        const intervalo = setInterval(() => {
            const ahora = new Date().getTime();
            const diferencia = fechaEvento - ahora;

            if (diferencia <= 0) {
                clearInterval(intervalo);
  
                contenedor.textContent = "¡El evento ya comenzó!"; 
                return;
            }


            const dias = Math.floor(diferencia / (1000 * 60 * 60 * 24));
            const horas = Math.floor((diferencia % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutos = Math.floor((diferencia % (1000 * 60 * 60)) / (1000 * 60));
            const segundos = Math.floor((diferencia % (1000 * 60)) / 1000);


            contenedor.textContent = `${dias}D: ${horas}H: ${minutos}M: ${segundos}S`;
        }, 1000);
    };


    contenedores.forEach(iniciarCountdown);
});