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
 
 
    
@app.route('/data_for_filters/<file_id>', methods=['POST'])
def get_data_for_filters(file_id):
    if file_id in uploaded_data:
        data = request.get_json()
        if data and 'columns' in data:
            selected_columns = data['columns']
            df = uploaded_data[file_id][selected_columns]
            numeric_columns = [col for col in df.select_dtypes(include=['number']).columns if col in selected_columns]
            categorical_columns = [col for col in df.select_dtypes(include=['object', 'category']).columns if col in selected_columns]

            numeric_ranges = {col: {'min': float(df[col].min()), 'max': float(df[col].max())} for col in numeric_columns}
            categorical_values = {col: df[col].unique().tolist() for col in categorical_columns}

            return jsonify({
                'numeric_columns': numeric_columns,
                'categorical_columns': categorical_columns,
                'numeric_ranges': numeric_ranges,
                'categorical_values': categorical_values
            }), 200
        else:
            return jsonify({'error': 'No se especificaron las columnas'}), 400
    else:
        return jsonify({'error': 'File not found'}), 404

        
    
@app.route('/data/<file_id>', methods=['POST'])
def get_data(file_id):
    if file_id in uploaded_data:
        data = request.get_json()
        if data and 'columns' in data:
            selected_columns = data['columns']
            df = uploaded_data[file_id][selected_columns].copy() # Importante usar .copy() para evitar SettingWithCopyWarning

            filters = data.get('filters', {})
            for col, filter_info in filters.items():
                if filter_info['type'] == 'numeric_range':
                    min_val, max_val = filter_info['value']
                    df = df[(df[col] >= min_val) & (df[col] <= max_val)]
                elif filter_info['type'] == 'categorical':
                    selected_values = filter_info['value']
                    if selected_values:
                        df = df[df[col].isin(selected_values)]

            data_json = df.to_dict(orient='records')
            return jsonify(data_json), 200
        else:
            return jsonify({'error': 'No se especificaron las columnas'}), 400
    else:
        return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
