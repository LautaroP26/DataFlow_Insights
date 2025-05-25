import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px  # Para gráficos interactivos

st.title("DataFlow Insights")
uploaded_file = st.file_uploader("Carga tu archivo de datos (CSV)", type=["csv"])

backend_url = "http://127.0.0.1:5000"

if uploaded_file is not None:
    files = {"file": uploaded_file}
    try:
        response = requests.post(f"{backend_url}/upload", files=files)
        response.raise_for_status()
        uploaded_result = response.json()
        if "file_id" in uploaded_result:
            file_id = uploaded_result["file_id"]
            st.session_state['file_id'] = file_id
            st.session_state['mostrar_columnas'] = True
        else:
            st.error(f"Error al cargar el archivo: {uploaded_result.get('error', 'Error desconocido')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexion con el backend: {e}")
    except json.JSONDecodeError:
        st.error("Error al decodificar la respuesta del backend.")

if st.session_state.get('mostrar_columnas'):
    file_id = st.session_state.get('file_id')
    if file_id:
        try:
            response_columns = requests.get(f"{backend_url}/columnas/{file_id}")
            response_columns.raise_for_status()
            columnas_resultado = response_columns.json()
            if "columnas" in columnas_resultado:
                columnas = columnas_resultado["columnas"]
                st.subheader("Columnas disponibles:")
                selected_columns = st.multiselect("Selecciona las columnas a analizar", columnas)
                if selected_columns:
                    st.subheader("Opciones de Visualización:")
                    chart_type = st.selectbox("Selecciona el tipo de gráfico",
                                                ["Histograma", "Gráfico de Dispersión", "Gráfico de Barras",
                                                 "Gráfico de Líneas", "Gráfico de Pastel"])

                    st.subheader("Datos:")
                    data_payload = {'columns': selected_columns}
                    response_data = requests.post(f"{backend_url}/data/{file_id}", json=data_payload)
                    response_data.raise_for_status()
                    data_result = response_data.json()
                    df = pd.DataFrame(data_result) # Convertir a DataFrame para facilitar la visualización

                    if chart_type == "Histograma":
                        if len(selected_columns) >= 1 and pd.api.types.is_numeric_dtype(df[selected_columns[0]]):
                            title = st.text_input("Titulo de Historigrama: ", f"Distribucion de {selected_columns[0]}")
                            fig = px.histogram(df, x=selected_columns[0], title=title)
                            st.plotly_chart(fig)
                        else:
                            st.warning("Selecciona al menos una columna numérica para el histograma.")
                    elif chart_type == "Gráfico de Dispersión":
                        if len(selected_columns) >= 2 and all(pd.api.types.is_numeric_dtype(df[col]) for col in selected_columns[:2]):
                            x_col = st.selectbox("Selecciona la columna para el eje X", selected_columns)
                            y_col = st.selectbox("Selecciona la columna para el eje Y", [col for col in selected_columns if col != x_col])
                            title = st.time_input("Titulo de dispercion:", f'Distribucion de {selected_columns[0]}')
                            fig = px.scatter(df, x=x_col, y=y_col, title=title)
                            st.plotly_chart(fig)
                        else:
                            st.warning("Selecciona al menos dos columnas numéricas para el gráfico de dispersión.")
                    elif chart_type == "Gráfico de Barras":
                        if len(selected_columns) >= 2:
                            x_col = st.selectbox("Selecciona la columna para las categorías (X)", selected_columns)
                            y_col = st.selectbox("Selecciona la columna para los valores (Y)", [col for col in selected_columns if col != x_col])
                            title = st.text_input("Titulo del grafico de Dispercion: ", f"{y_col} vs {x_col}")
                            fig = px.scatter(df, x=x_col, y=y_col, title=title)
                            st.plotly_chart(fig)
                        else:
                            st.warning("Selecciona al menos dos columnas para el gráfico de barras.")
                    elif chart_type == "Gráfico de Líneas":
                        if len(selected_columns) >= 2:
                            x_col = st.selectbox("Selecciona la columna para el eje X", selected_columns)
                            y_col = st.selectbox("Selecciona la columna para el eje Y", [col for col in selected_columns if col != x_col])
                            title = st.text_input("Titulo del grafico de Líneas: ", f"{x_col} vs {y_col}")
                            fig = px.line(df, x=x_col, y=y_col, title=title)
                            st.plotly_chart(fig)
                        else:
                            st.warning("Selecciona al menos dos columnas para el gráfico de líneas.")
                    elif chart_type == "Gráfico de Pastel":
                        if len(selected_columns) == 2:
                            categorical_col = st.selectbox("Selecciona la columna Categórica", selected_columns)
                            value_col = st.selectbox("Selecciona la columna de Valores", [col for col in selected_columns if col != categorical_col])
                            title = st.text_input("Titulo del grafico de Torta", f'Porcion de {categorical_col} por {value_col}')
                            fig = px.pie(df, names=categorical_col, values=value_col, title=title)
                            st.plotly_chart(fig)
                        else:
                            st.warning("Selecciona al menos dos columnas para el gráfico de Pastel")

            else:
                st.error(f"Error al obtener las columnas: {columnas_resultado.get('error', 'Error desconocido')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error de conexion con el backend: {e}")
        except json.JSONDecodeError:
            st.error("Error al decodificar la respuesta del backend.")
    else:
        st.info("Carga un archivo CSV para ver las columnas disponibles.")
else:
    st.info("Carga un archivo CSV para ver las columnas disponibles.")