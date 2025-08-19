// Base del backend en tu VM (pon tu host real)
// Ejemplos:
//   https://158-158-16-44.sslip.io   (si ya hiciste certbot)
//   http://158.158.16.44             (solo para pruebas; SWA en HTTPS lo bloqueará)
export const API_BASE = 'https://158-158-16-44.sslip.io';

export const IMG_BASE = `${API_BASE}/imagenes/`;
const API_URL = `${API_BASE}/api/buscar`;

export async function buscarPersonas(descripcion, numResultados) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ descripcion, numResultados })
  });
  if (!response.ok) throw new Error('Error en la petición');
  return response.json();
}
