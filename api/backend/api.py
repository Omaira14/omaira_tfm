# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from busqueda_imagnes import buscar_imagenes_por_descripcion

# app = Flask(__name__)
# CORS(app)  # Permitir CORS para peticiones desde el frontend

# @app.route('/api/buscar', methods=['POST'])
# def buscar():
#     print("[API] Petición recibida")
#     data = request.get_json()
#     print(f"[API] Datos recibidos: {data}")
#     descripcion = data.get('descripcion', '')
#     num_resultados = int(data.get('numResultados', 5))
#     print(f"[API] Ejecutando búsqueda: descripción='{descripcion}', num_resultados={num_resultados}")
#     try:
#         resultados = buscar_imagenes_por_descripcion(descripcion, num_resultados)
#         print(f"[API] Resultados encontrados: {len(resultados)}")
#         return jsonify(resultados)
#     except Exception as e:
#         print(f"[API] Error durante la búsqueda: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/imagenes/<filename>')
# def servir_imagen(filename):
#     return send_from_directory('imagenes', filename)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)



# api/backend/api.py
import os
from urllib.parse import quote            # <-- importa quote
from flask import Flask, request, jsonify, redirect   # <-- importa redirect
from flask_cors import CORS
from busqueda_imagnes import buscar_imagenes_por_descripcion

app = Flask(__name__)
CORS(app)

# Variables (ponlas también en SWA > Configuration)
STORAGE_ACCOUNT = os.getenv('STORAGE_ACCOUNT', 'TU_CUENTA')   # ej. imagenes550
STORAGE_CONTAINER = os.getenv('STORAGE_CONTAINER', 'imagenes')
BLOB_PREFIX = os.getenv('BLOB_PREFIX', '')   # deja '' si no usas subcarpeta

@app.route('/api/buscar', methods=['POST'])
def buscar():
    data = request.get_json() or {}
    descripcion = data.get('descripcion', '')
    num_resultados = int(data.get('numResultados', 5))
    try:
        resultados = buscar_imagenes_por_descripcion(descripcion, num_resultados)
        return jsonify(resultados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/imagenes/<path:filename>')
def servir_imagen(filename):
    # compón la ruta dentro del contenedor (añade prefijo si lo usas)
    path_inside_container = f"{BLOB_PREFIX}{filename}".lstrip('/')
    blob_url = (
        f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/"
        f"{STORAGE_CONTAINER}/{quote(path_inside_container)}"
    )
    return redirect(blob_url, code=302)