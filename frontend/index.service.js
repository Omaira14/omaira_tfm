// Servicio para gestionar peticiones a la API
const API_URL = 'http://158.158.16.44';

export async function buscarPersonas(descripcion, numResultados) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ descripcion, numResultados })
  });
  if (!response.ok) throw new Error('Error en la petición');
  return await response.json();
}
