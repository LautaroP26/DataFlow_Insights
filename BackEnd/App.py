from flask import Flask, request, jsonify
import pandas as pd
import os
import uuid


#Crea una instancia de la aplicación Flask
app = Flask(__name__)
uploaded_data = {}  # Diccionario para almacenar DataFrames cargados

#Define la ruta para la carga de archivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:    
        #Manejo de errores
        try:
            df = pd.read_csv(file)
            file_id = str(uuid.uuid4())
            uploaded_data[file_id] = df
            return jsonify({'Mensaje': 'Archivo cargado exitosamente', 'file_id': file_id}), 200
        except pd.errors.ParserError as e:
            return jsonify({'error': f'Error de Pandas al leer el CSV: {str(e)}'}), 400
        except UnicodeDecodeError as e:
            return jsonify({'error': f'Error de codificación del archivo: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': f'Error general al procesar el archivo: {str(e)}'}), 500
    return jsonify({'error': 'Algo salió mal'}), 500

@app.route('/columnas/<archi_id>', methods=['GET'])
def get_columns(archi_id):
    if archi_id in uploaded_data:
        df = uploaded_data[archi_id]
        columnas = df.columns.tolist()
        return jsonify({'columnas':columnas}), 200
    else:
        return jsonify({'error':'Archivo no encontrado'}), 404
    
    
@app.route('/data/<file_id>' , methods=['POST'])
def get_data(file_id):
    if file_id in uploaded_data:
        data = request.get_json()
        if data and 'columns' in data:
            selected_columns = data['columns']
            df = uploaded_data[file_id][selected_columns]
            #Convierte el DataFrame a un formato JSON seria listable
            data_json = df.to_dict(orient='records')
            return jsonify(data_json), 200
        else:
            return jsonify({'error':'No se especificaron las columnas'}), 400
    else:
        return jsonify({'error': 'Archivo no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
