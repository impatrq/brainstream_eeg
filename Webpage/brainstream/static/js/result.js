// var imagen = document.getElementById('logochange');
// logochange.src =  "/static/img/logo-negro.png";
longitud = 300
function cambiarIcono() {
    // iconoElemento = document.getElementById("icono1");

    if (iconoElemento1.classList.contains("fa-record-vinyl")) {
        iconoElemento1.classList.remove("fa-record-vinyl");
        iconoElemento1.classList.add("fa-stop");
    } else {
        iconoElemento1.classList.remove("fa-stop");
        iconoElemento1.classList.add("fa-record-vinyl");
    }
}
function cambiarIcono1() {

    // iconoElemento = document.getElementById("icono");
    if (iconoElemento.classList.contains("fa-pause")) {
        iconoElemento.classList.remove("fa-pause");
        iconoElemento.classList.add("fa-play");
    } else {
        iconoElemento.classList.remove("fa-play");
        iconoElemento.classList.add("fa-pause");
    }
}


window.addEventListener("scroll", function () {
    var lb = document.querySelector("lat_butons");
    lb.classList.toggle("sticky", window.scrollY > 0);
})

var username = document.getElementById('my-element').getAttribute('data-my-variable');
var presion = 0
var range = "";
var cadena = "";
var enviado = 0;
var data_send = {
    "presion": presion,
    "username": username
}
for (var i = 0; i < 400; i++) {
    range += i.toString() + ", ";
    cadena += i.toString() + ", ";
} { }
var arrayEnteros = cadena.split(",").map(function (num) {
    return parseInt(num.trim(), 10);
});
var arrayStrings = range.split(",").map(function (str) {
    return str.trim();
});

var iconoElemento = document.getElementById("icono");
var iconoElemento1 = document.getElementById("icono1");
var ctx1 = document.getElementById('myChart1').getContext('2d');
var ctx2 = document.getElementById('myChart2').getContext('2d');
var ctx3 = document.getElementById('myChart3').getContext('2d');
var ctx4 = document.getElementById('myChart4').getContext('2d');
var ctx5 = document.getElementById('myChart5').getContext('2d');
var ctx6 = document.getElementById('myChart6').getContext('2d');
var ctx7 = document.getElementById('myChart7').getContext('2d');
var ctx8 = document.getElementById('myChart8').getContext('2d');
var ctx9 = document.getElementById('myChart9').getContext('2d');
var ctx10 = document.getElementById('myChart10').getContext('2d');
var ctx11 = document.getElementById('myChart11').getContext('2d');
var ctx12 = document.getElementById('myChart12').getContext('2d');
var ctx13 = document.getElementById('myChart13').getContext('2d');
var ctx14 = document.getElementById('myChart14').getContext('2d');
var ctx15 = document.getElementById('myChart15').getContext('2d');
var ctx16 = document.getElementById('myChart16').getContext('2d');
var mensajeElement = document.getElementById("mensaje")
var mensajeElement2 = document.getElementById("mensaje2");
function createGraphData(label) {
    return {
        type: 'line',
        options: {
            animation: {
                duration: 0,
            },
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    enabled: false,
                },
            },
            hover: {
                mode: null
            },
            elements: {
                point: {
                    radius: 0,
                },
            },
            scales: {
                x: {
                    type: 'linear',
                    min: 0,
                    max: 400,
                    grid: {
                        display: true,
                        drawOnChartArea: false,
                        drawTicks: false,
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        display: false
                    }
                },
                y: {
                    grid: {
                        display: true,
                        drawOnChartArea: false,
                        drawTicks: false,
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        display: false
                    },
                    min: 0,
                    max: 3,
                }
            },
            responsive: true,
            maintainAspectRatio: false,
        },
        data: {
            labels: arrayStrings,
            datasets: [{
                label: label,
                data: [],
                backgroundColor: 'rgb(75, 192, 192)',
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 1,
                fill: false,
            }],
        },
    };
}

var myChart1 = new Chart(ctx1, graphData1);
var myChart2 = new Chart(ctx2, graphData2);
var myChart3 = new Chart(ctx3, graphData3);
var myChart4 = new Chart(ctx4, graphData4);
var myChart5 = new Chart(ctx5, graphData5);
var myChart6 = new Chart(ctx6, graphData6);
var myChart7 = new Chart(ctx7, graphData7);
var myChart8 = new Chart(ctx8, graphData8);
var myChart9 = new Chart(ctx9, graphData9);
var myChart10 = new Chart(ctx10, graphData10);
var myChart11 = new Chart(ctx11, graphData11);
var myChart12 = new Chart(ctx12, graphData12);
var myChart13 = new Chart(ctx13, graphData13);
var myChart14 = new Chart(ctx14, graphData14);
var myChart15 = new Chart(ctx15, graphData15);
var myChart16 = new Chart(ctx16, graphData16);

var socket = null;

socket = new WebSocket("ws://localhost:8000/menu/resultn");


var dataValue = []
var presion = 0
// var gradient = ctx.createLinearGradient(graphData.options.width / 2, graphData.options.height, graphData.options.width / 2, 0);
myChart1.data.datasets[0].borderColor = "blue"
myChart2.data.datasets[0].borderColor = "lightblue"
myChart3.data.datasets[0].borderColor = "green"
myChart4.data.datasets[0].borderColor = "lawngreen"
myChart5.data.datasets[0].borderColor = "yellow"
myChart6.data.datasets[0].borderColor = "orange"
myChart7.data.datasets[0].borderColor = "red"
myChart8.data.datasets[0].borderColor = "pink"
myChart9.data.datasets[0].borderColor = "purple"
myChart10.data.datasets[0].borderColor = "salmon"
myChart11.data.datasets[0].borderColor = "brown"
myChart12.data.datasets[0].borderColor = "teal"
myChart13.data.datasets[0].borderColor = "hotpink"
myChart14.data.datasets[0].borderColor = "aquamarine"
myChart15.data.datasets[0].borderColor = "grey"
myChart16.data.datasets[0].borderColor = "black"
// gradient.addColorStop(0, 'rgba(75, 192, 192, 1)'); // Color en la línea
// gradient.addColorStop(1, 'rgba(75, 192, 192, 0)'); // Color transparente en el punto 0 del eje y

// graphData.data.datasets[0].backgroundColor = gradient;
socket.onmessage = function (e) {
    var djangoData = JSON.parse(e.data);
    var frequency = djangoData.sfreq;
    var counter = djangoData.counter;
    dataValue = dataValue.concat(djangoData.value);
    // console.log(dataValue);
    // dataValue.push(djangoData.value);
    if (dataValue.length >= 300) {
        // dataValue.shift();
        // dataValue.shift(0, dataValue.length);
        dataValue.splice(0, dataValue.length - 300);
    }
    // dataValue = djangoData.value
    
    myChart1.data.datasets[0].data = dataValue;
    myChart2.data.datasets[0].data = dataValue;
    myChart3.data.datasets[0].data = dataValue;
    myChart4.data.datasets[0].data = dataValue;
    myChart5.data.datasets[0].data = dataValue;
    myChart6.data.datasets[0].data = dataValue;
    myChart7.data.datasets[0].data = dataValue;
    myChart8.data.datasets[0].data = dataValue;
    myChart9.data.datasets[0].data = dataValue;
    myChart10.data.datasets[0].data = dataValue;
    myChart11.data.datasets[0].data = dataValue;
    myChart12.data.datasets[0].data = dataValue;
    myChart13.data.datasets[0].data = dataValue;
    myChart14.data.datasets[0].data = dataValue;
    myChart15.data.datasets[0].data = dataValue;
    myChart16.data.datasets[0].data = dataValue;
    mensajeElement.innerText = frequency;
    mensajeElement2.innerText = counter;
    if (!iconoElemento.classList.contains("fa-pause")) {
        myChart1.update();
        myChart2.update();
        myChart3.update();
        myChart4.update();
        myChart5.update();
        myChart6.update();
        myChart7.update();
        myChart8.update();
        myChart9.update();
        myChart10.update();
        myChart11.update();
        myChart12.update();
        myChart13.update();
        myChart14.update();
        myChart15.update();
        myChart16.update();
    } 
    if (iconoElemento1.classList.contains("fa-record-vinyl")) {
        presion = 0;
    } else {
        presion = 1;
    }
    socket.send(presion);
    // socket.send('message');
};

function generarValoresAleatorios() {
    var valores = [];
    var minValue = 0;
    var maxValue = 500;
    for (var i = 0; i < 400; i++) {
        var randomValue = Math.floor(Math.random() * (maxValue - minValue + 1)) + minValue;
        valores.push(randomValue);
    }
    return valores;
}

function cerrarSesionYRedirigir(buttonId) {
    // Obtener el objeto WebSocket
    // Manejar el evento de conexión establecida
    socket.onopen = function () {
        console.log('Conexión establecida');
        // Enviar un mensaje al servidor WebSocket
        var message = 'Cerrar sesión';
        socket.send(message);
    };
    window.location.href = 'http://127.0.0.1:8000/menu/' + buttonId
    socket.close();

}

socket.onclose = function () {
    // La conexión WebSocket se cerró
    socket.close();
};