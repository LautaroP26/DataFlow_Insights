window.plotlyInterop = {
    newPlot: function (elementId, data, layout, config) {
        Plotly.newPlot(elementId, data, layout || {}, config || {});
    },
    react: function (elementId, data, layout, config) {
        Plotly.react(elementId, data, layout || {}, config || {});
    },
    purge: function (elementId) {
        Plotly.purge(elementId);
    },
    // Función genérica para crear diferentes tipos de gráficos
    // Los datos y el layout deben ser preparados en C# según el tipo de gráfico
    createOrUpdateChart: function (elementId, chartType, traces, layout) {
        console.log("Creating or updating chart:", elementId, chartType, traces, layout);
        try {
            Plotly.react(elementId, traces, layout || {});
        } catch (e) {
            console.error("Plotly error:", e);
        }
    }
};
