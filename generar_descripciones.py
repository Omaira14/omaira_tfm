import os
import pandas as pd
from PIL import Image
from tqdm import tqdm
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Cargar modelo BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Usa la CPU (más estable en Mac M1)
device = torch.device("cpu")
model.to(device)

# Ruta de tu carpeta con imágenes
ruta_imagenes = "/Users/omairagonzalezperez/Desktop/tfm/imagenes"
extensiones_validas = [".jpg", ".jpeg", ".png", ".webp", ".bmp"]

# Preparar resultados
resultados = []

# Procesar cada imagen
for archivo in tqdm(os.listdir(ruta_imagenes)):
    if any(archivo.lower().endswith(ext) for ext in extensiones_validas):
        ruta_img = os.path.join(ruta_imagenes, archivo)
        imagen = Image.open(ruta_img).convert("RGB")

        inputs = processor(images=imagen, return_tensors="pt").to(device)
        output = model.generate(**inputs, max_new_tokens=20)
        descripcion = processor.decode(output[0], skip_special_tokens=True)

        resultados.append({"imagen": archivo, "descripcion": descripcion})

# Guardar resultados en CSV
df = pd.DataFrame(resultados)
df.to_csv("descripciones_generadas.csv", index=False)

print("✅ Descripciones guardadas en descripciones_generadas.csv")
