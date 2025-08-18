import os
import pandas as pd
from PIL import Image
from tqdm import tqdm
import torch
import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity



# Refactorización para uso como función/API

def buscar_imagenes_por_descripcion(descripcion, top_n=5, carpeta_imagenes="imagenes/"):
    print(f"[BUSQUEDA] Iniciando búsqueda para: '{descripcion}' | top_n={top_n}")
    print(f"[BUSQUEDA] Escaneando carpeta de imágenes: {carpeta_imagenes}")
    
    # Obtener todas las imágenes de la carpeta
    extensiones_validas = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
    imagenes_en_carpeta = []
    
    if not os.path.exists(carpeta_imagenes):
        print(f"[BUSQUEDA] ❌ Carpeta de imágenes no encontrada: {carpeta_imagenes}")
        return []
    
    for archivo in os.listdir(carpeta_imagenes):
        if archivo.lower().endswith(extensiones_validas):
            imagenes_en_carpeta.append(archivo)
    
    print(f"[BUSQUEDA] Encontradas {len(imagenes_en_carpeta)} imágenes")
    
    if not imagenes_en_carpeta:
        print("[BUSQUEDA] ❌ No se encontraron imágenes válidas en la carpeta.")
        return []
    
    print(f"[BUSQUEDA] Cargando modelo CLIP...")
    modelo = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    procesador = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    print(f"[BUSQUEDA] Procesando descripción del usuario...")
    inputs_texto = procesador(text=[descripcion], return_tensors="pt", padding=True)
    with torch.no_grad():
        embedding_texto = modelo.get_text_features(**inputs_texto)
        embedding_texto = F.normalize(embedding_texto, p=2, dim=1)

    print(f"[BUSQUEDA] Procesando imágenes...")
    embeddings_imagenes = []
    imagenes_validas = []
    
    for archivo_imagen in tqdm(imagenes_en_carpeta, desc="Procesando imágenes"):
        path_completo = os.path.join(carpeta_imagenes, archivo_imagen)
        try:
            imagen = Image.open(path_completo).convert("RGB")
            inputs_imagen = procesador(images=imagen, return_tensors="pt")
            with torch.no_grad():
                embedding_imagen = modelo.get_image_features(**inputs_imagen)
                embedding_imagen = F.normalize(embedding_imagen, p=2, dim=1)
            embeddings_imagenes.append(embedding_imagen)
            imagenes_validas.append(archivo_imagen)
        except Exception as e:
            print(f"[BUSQUEDA] Error procesando imagen {archivo_imagen}: {e}")

    if not embeddings_imagenes:
        print("[BUSQUEDA] ❌ No se pudo procesar ninguna imagen.")
        return []

    print(f"[BUSQUEDA] Calculando similitudes...")
    embeddings_tensor = torch.cat(embeddings_imagenes)
    similitudes = torch.matmul(embedding_texto, embeddings_tensor.T)[0].cpu().numpy()
    
    # Crear lista de resultados con similitudes
    resultados_con_similitud = []
    for i, imagen in enumerate(imagenes_validas):
        resultado = {
            "imagen": imagen,
            "similitud": float(similitudes[i])
        }
        print(f"[BUSQUEDA] Resultado {i+1}: {resultado}")  # Debug
        resultados_con_similitud.append(resultado)
    
    # Ordenar por similitud descendente y tomar top_n
    resultados_con_similitud.sort(key=lambda x: x["similitud"], reverse=True)
    top_resultados = resultados_con_similitud[:top_n]

    print(f"[BUSQUEDA] Resultados listos. Total: {len(top_resultados)}")
    print(f"[BUSQUEDA] Top resultados finales: {top_resultados}")  # Debug final
    return top_resultados

# Ejemplo de uso:
if __name__ == "__main__":
    descripcion_base = "Introduce aquí la descripción desde el frontend"
    top_n = 5  # O el valor recibido desde el frontend
    resultados = buscar_imagenes_por_descripcion(descripcion_base, top_n)
    print("\n📊 Top imágenes más parecidas:")
    for i, r in enumerate(resultados, 1):
        print(f"\n#{i}")
        print("Nombre:", r["imagen"])
        print("Descripción:", r["descripcion"])
        print("Similitud:", r["similitud"])
