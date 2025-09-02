// Base del backend en tu VM con certificado válido
export const API_BASE = 'https://omairatfm.spaincentral.cloudapp.azure.com';

// Ruta base para las imágenes
export const IMG_BASE = `${API_BASE}/imagenes/`;

// Endpoint de búsqueda
const API_URL = `${API_BASE}/api/buscar`;

// Función para buscar personas por descripción
export async function buscarPersonas(descripcion, numResultados) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ descripcion, numResultados })
  });

  if (!response.ok) {
    throw new Error('Error en la petición');
  }

  return response.json();
}
