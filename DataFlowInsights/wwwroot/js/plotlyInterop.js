window.plotlyInterop = {
    newPlot: function (elementId, data, layout, config) {
        var gd = document.getElementById(elementId);
        if (gd) {
            Plotly.newPlot(elementId, data, layout || {}, config || {});
        } else {
            console.warn("Plotly.newPlot skipped: Element " + elementId + " not found.");
        }
    },
    react: function (elementId, data, layout, config) {
        var gd = document.getElementById(elementId);
        if (gd) {
            Plotly.react(elementId, data, layout || {}, config || {});
        } else {
            console.warn("Plotly.react skipped: Element " + elementId + " not found.");
        }
    },
    purge: function (elementId) {
        var gd = document.getElementById(elementId);
        // gd._fullLayout es una forma de verificar si Plotly ha dibujado algo en este div anteriormente.
        // Si el div no existe, o si Plotly nunca ha dibujado en él, no hay nada que purgar.
        if (gd && gd._fullLayout) {
            Plotly.purge(elementId);
        } else {
            console.log("Plotly.purge skipped: Element " + elementId + " not found or not a Plotly graph.");
        }
    },
    createOrUpdateChart: function (elementId, chartType, traces, layout) {
        var gd = document.getElementById(elementId);
        if (!gd) {
            console.error("Plotly.createOrUpdateChart error: Element " + elementId + " not found.");
            return; // Detener si el elemento no existe
        }
        console.log("Creating or updating chart:", elementId, chartType, traces, layout);
        try {
            Plotly.react(elementId, traces, layout || {});
        } catch (e) {
            console.error("Plotly error:", e);
        }
    }
};
