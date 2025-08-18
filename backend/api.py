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



from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
# ¡OJO al nombre del módulo!
# En tu captura era 'busqueda_imagenes.py', aquí estaba escrito 'busqueda_imagnes'
from busqueda_imagnes import buscar_imagenes_por_descripcion

app = Flask(__name__)
CORS(app)

@app.route('/api/buscar', methods=['POST'])
def buscar():
    data = request.get_json()
    descripcion = data.get('descripcion', '')
    num_resultados = int(data.get('numResultados', 5))
    try:
        resultados = buscar_imagenes_por_descripcion(descripcion, num_resultados)
        return jsonify(resultados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Antes: '/imagenes/<filename>'
@app.route('/api/imagenes/<filename>')
def servir_imagen(filename):
    # 'imagenes' se toma relativo a la carpeta del paquete 'backend'
    # si este archivo está en backend/, funciona tal cual.
    return send_from_directory('imagenes', filename)
