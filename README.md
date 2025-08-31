# 📊 DataFlow Insights (.NET Version)

**DataFlow Insights** es una aplicación web interactiva para el análisis y visualización de datos CSV. Esta versión ha sido desarrollada utilizando .NET y Blazor Server, ofreciendo una interfaz de usuario dinámica para cargar archivos, aplicar filtros y generar diversos tipos de gráficos en tiempo real.

---

## 🚀 Objetivos del Proyecto

- Permitir a los usuarios cargar archivos CSV y explorar sus datos de forma interactiva.
- Ofrecer funcionalidades de filtrado por columnas numéricas y categóricas.
- Visualizar datos mediante gráficos personalizables (histogramas, dispersión, barras, líneas, pastel).
- Demostrar la creación de aplicaciones web interactivas con .NET y Blazor.

---

## 🧰 Herramientas Utilizadas

- **.NET (6.0 o superior)**
- **C#**
- **ASP.NET Core Blazor Server** para la interfaz de usuario interactiva.
- **CsvHelper** para la lectura y parseo de archivos CSV.
- **Plotly.js** para la generación de gráficos interactivos en el cliente.
- **Git & GitHub** para control de versiones y documentación.

---

## 🗂 Estructura del Repositorio

DataFlow_Insights/
│
├── DataFlowInsights/ # Proyecto principal ASP.NET Core Blazor
│   ├── Data/ # Servicios de datos, modelos
│   │   ├── DataService.cs
│   │   ├── FileData.cs
│   │   └── FilterModels.cs
│   ├── Pages/ # Componentes Razor para las páginas
│   │   ├── Index.razor
│   │   ├── _Host.cshtml
│   │   └── _Layout.cshtml
│   ├── Properties/
│   │   └── launchSettings.json
│   ├── Shared/ # Componentes Razor compartidos
│   │   ├── MainLayout.razor
│   │   ├── NavMenu.razor
│   │   └── SurveyPrompt.razor (Ejemplo, podría eliminarse)
│   ├── wwwroot/ # Archivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   │   └── plotlyInterop.js
│   │   └── favicon.ico
│   ├── App.razor
│   ├── DataFlowInsights.csproj
│   ├── Program.cs
│   └── _Imports.razor
│
├── Data/ # Carpeta para ejemplos de datos CSV
│   ├── LISTADO PARA CAMBIO DE LISTA 2-1-23.csv
│   └── annual-enterprise-survey-2023-financial-year-provisional-size-bands.csv
│
├── Proyecto DataFlow_Insights.txt # Documento de planificación original (puede ser obsoleto)
│
└── README.md # Esta documentación

---

## 📌 Alcance

Esta aplicación permite:

- **Carga de Archivos CSV:** Los usuarios pueden subir sus propios archivos CSV.
- **Selección de Columnas:** Elegir qué columnas del CSV analizar y mostrar.
- **Filtrado de Datos:**
    - Aplicar filtros de rango a columnas numéricas.
    - Aplicar filtros de selección múltiple a columnas categóricas.
- **Visualización de Datos:**
    - Mostrar los datos filtrados en una tabla.
    - Generar gráficos interactivos: Histogramas, Gráficos de Dispersión, Gráficos de Barras, Gráficos de Líneas y Gráficos de Pastel.
- **Interfaz Interactiva:** La UI se actualiza dinámicamente según las selecciones del usuario.

---

## ⚠️ Limitaciones del Proyecto (Versión Actual)

- **Manejo de Errores:** Aunque se ha implementado un manejo básico, podría ser más robusto y específico para diferentes escenarios de datos malformados.
- **Rendimiento con Archivos Muy Grandes:** El procesamiento de CSV se realiza en memoria del servidor. Para archivos extremadamente grandes, el rendimiento podría degradarse.
- **Detección de Tipos de Columna:** La detección automática entre tipos numéricos y categóricos en `DataService` es una simplificación y podría no cubrir todos los casos borde.
- **Componentes de UI para Filtros:** Los filtros numéricos usan inputs estándar; sliders visuales podrían mejorar la experiencia. El multiselect categórico es un `<select multiple>` estándar.
- **Personalización de Gráficos:** Las opciones de personalización de gráficos (colores, etiquetas avanzadas, etc.) son limitadas en la UI actual.
- **Pruebas Automatizadas:** No se han implementado pruebas unitarias o de integración.
- **Despliegue:** Diseñado para ejecución local. Para producción, se necesitarían consideraciones adicionales (Docker, configuración de servidor web, etc.).

---

## 🛠️ Cómo Ejecutarlo

1.  **Requisitos Previos:**
    *   SDK de .NET (versión 6.0 o superior). [Descargar .NET SDK](https://dotnet.microsoft.com/download)
    *   Un editor de código o IDE (Visual Studio, VS Code, JetBrains Rider).

2.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/LautaroP26/DataFlow_Insights.git
    cd DataFlow_Insights
    ```

3.  **Navega a la carpeta del proyecto:**
    ```bash
    cd DataFlowInsights
    ```

4.  **Restaurar dependencias (si es necesario):**
    Aunque `CsvHelper` se añadió al `.csproj`, si es la primera vez o cambiaste dependencias, ejecuta:
    ```bash
    dotnet restore
    ```

5.  **Ejecutar la aplicación:**
    ```bash
    dotnet run
    ```
    Esto iniciará la aplicación. Por defecto, estará disponible en `https://localhost:5001` o `http://localhost:5000` (revisa la salida de la consola para la URL exacta).

6.  **Abrir en el navegador:**
    Abre tu navegador web y navega a la URL proporcionada por la consola (ej. `https://localhost:5001`).

7.  **Uso:**
    *   Utiliza el botón "Carga tu archivo de datos (CSV)" para subir un archivo.
    *   Selecciona las columnas que deseas analizar.
    *   Aplica filtros en la sección "Filtros".
    *   Observa los datos filtrados en la tabla.
    *   Elige un tipo de gráfico, configura sus columnas y título, y haz clic en "Generar Gráfico".

---

## 🧭 Próximos Pasos / Roadmap

- **Mejorar Componentes de UI:** Implementar sliders para filtros numéricos y un componente multiselect más amigable para filtros categóricos.
- **Opciones Avanzadas de Gráficos:** Permitir más personalización en los gráficos (colores, leyendas, tipos de agregación).
- **Manejo de Errores Mejorado:** Proveer feedback más detallado al usuario sobre problemas con los datos o la configuración.
- **Optimización de Rendimiento:** Investigar técnicas de streaming o procesamiento por lotes para archivos CSV muy grandes.
- **Persistencia de Sesión (Opcional):** Guardar el estado de la sesión del usuario (archivo cargado, filtros) para que no se pierda al recargar.
- **Pruebas Automatizadas:** Añadir pruebas unitarias para `DataService` y, potencialmente, pruebas de UI con Playwright o Selenium.
- **Contenerización (Docker):** Facilitar el despliegue y la portabilidad.

## 👤 Sobre el Autor
 # Lautaro P.
📍 Apasionado por los datos y en formación constante como Data Analyst y desarrollador.
💼 Este proyecto forma parte de mi portafolio profesional.
🔗 www.linkedin.com/in/lautaro-pedernera-91ba821bb

## 📄 Licencia
Este proyecto está bajo la licencia MIT. Es de libre uso, distribución y modificación.

*“La intuición gana con la experiencia, pero el análisis gana con los datos.”*

