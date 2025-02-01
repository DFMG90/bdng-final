document.getElementById("form").addEventListener("submit", async (event) => {
    event.preventDefault(); // Evita que el formulario se recargue

    const idCliente = document.getElementById("idCliente").value;
    const idProducto = document.getElementById("idProducto").value;
    const rating = document.getElementById("rating").value;

    // Construye la URL con los parámetros
    const url = `https://7s98pr5chh.execute-api.eu-west-3.amazonaws.com/rate?rating=${idCliente}&${rating}&${idProducto}`;

    try {
        const response = await fetch(url, {
            method: "GET", // O "POST" si tu API requiere un POST
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json(); // Procesa la respuesta como JSON
        console.log("¡Funciona! Conexión establecida."); // Muestra el mensaje de éxito en la consola
        console.log("Respuesta del API:", data);

        // Muestra la respuesta en el DOM
        document.getElementById("resultado").innerText = `¡Funciona! Conexión establecida. Respuesta del API: ${JSON.stringify(data)}`;
    } catch (error) {
        console.error("Error al llamar a la API:", error);
        document.getElementById("resultado").innerText = "Error al llamar a la API";
    }
});
