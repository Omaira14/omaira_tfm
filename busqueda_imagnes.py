import os
import pandas as pd
from PIL import Image
from tqdm import tqdm
import torch
import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity


# Carpeta donde están las imágenes
carpeta_imagenes = "imagenes/"

# Cargar CSV con columnas: 'imagen', 'descripcion'
df = pd.read_csv("descripciones_generadas.csv")

# Cargar modelo CLIP
modelo = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
procesador = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Obtener embedding de la primera descripción y normalizar
descripcion_base = df["descripcion"][0]
inputs_texto = procesador(text=[descripcion_base], return_tensors="pt", padding=True)
with torch.no_grad():
    embedding_texto = modelo.get_text_features(**inputs_texto)
    embedding_texto = F.normalize(embedding_texto, p=2, dim=1)  # L2 normalize

# Generar embeddings normalizados de las imágenes
embeddings_imagenes = []
imagenes_validas = []

for ruta in tqdm(df["imagen"], desc="Procesando imágenes"):
    path_completo = os.path.join(carpeta_imagenes, ruta)
    if not os.path.exists(path_completo):
        print(f"⚠️ Imagen no encontrada: {path_completo}")
        continue
    imagen = Image.open(path_completo).convert("RGB")
    inputs_imagen = procesador(images=imagen, return_tensors="pt")
    with torch.no_grad():
        embedding_imagen = modelo.get_image_features(**inputs_imagen)
        embedding_imagen = F.normalize(embedding_imagen, p=2, dim=1)  # L2 normalize
    embeddings_imagenes.append(embedding_imagen)
    imagenes_validas.append(ruta)

# Verificación
if not embeddings_imagenes:
    print("❌ No se pudo procesar ninguna imagen.")
    exit()

# Crear nuevo DataFrame solo con imágenes válidas
df_validas = df[df["imagen"].isin(imagenes_validas)].reset_index(drop=True)

# Calcular similitudes coseno entre la descripción y todas las imágenes
embeddings_tensor = torch.cat(embeddings_imagenes)
similitudes = torch.matmul(embedding_texto, embeddings_tensor.T)[0].cpu().numpy()
df_validas["similitud"] = similitudes

# Mostrar TOP 5
top5 = df_validas.sort_values(by="similitud", ascending=False).head(5)

print("🔎 Descripción base:")
print(descripcion_base)
print("\n📊 Top 5 imágenes más parecidas:")
for i, row in top5.iterrows():
    print(f"\n#{i+1}")
    print("Nombre:", row["imagen"])
    print("Descripción:", row["descripcion"])
    print("Similitud:", row["similitud"])

# (Opcional) Mostrar visualmente la imagen más parecida
try:
    path_img_top = os.path.join(carpeta_imagenes, top5.iloc[0]["imagen"])
    img_top = Image.open(path_img_top)
except:
    pass
