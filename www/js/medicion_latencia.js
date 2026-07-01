let mediciones = [];
let contador = 0;

document.addEventListener("keydown", function(event) {
     const teclasValidas = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "z", "x", "Enter", " " ];

     if (!teclasValidas.includes(event.key)) {
	  return;
     }

     const inicio = performance.now();

     requestAnimationFrame(function() {
     const fin = performance.now();
     const latencia = fin - inicio;

     contador++;

     const registro = {
     prueba: contador,
     tecla: event.key,
     latencia_ms: latencia.toFixed(3),
     fecha: new Date().toISOString()
     };

     mediciones.push(registro);

     console.log("Prueba:", registro.prueba, "| Tecla:", registro.tecla, "| Latencia:", registro.latencia_ms, "ms");

	actualizarPanel(registro);
     });
});

function actualizarPanel(registro) {
     const panel = document.getElementById("panel-latencia");

     if (!panel) {
           return;
     }

     panel.innerHTML = "Última tecla: " + registro.tecla + " | Latencia: " + registro.latencia_ms + " ms" + " | Muestras: " + mediciones.length;

}

function descargarCSV() {
     if (mediciones.length === 0) {
           alert("Todavía no se han hecho las mediciones");
	   return;
     }

     let csv = "prueba,tecla,latencia_ms,fecha\n";

     mediciones.forEach(function(m) {
     csv += `${m.prueba},${m.tecla},${m.latencia_ms},${m.fecha}\n`;
     });

     const blob = new Blob([csv], { type: "text/csv" });
     const url = URL.createObjectURL(blob);

     const enlace = document.createElement("a");
     enlace.href = url;
     enlace.download = "latencias_emulador.csv";
     enlace.click();

     URL.revokeObjectURL(url);
}

window.descargarCSV = descargarCSV; 
